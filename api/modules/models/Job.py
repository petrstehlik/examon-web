import logging
import calendar
from datetime import datetime, timedelta
import decimal
import json

from muapi import config


class Job:
    """
    Difference PBSPro vs SLURM
        * back_qtime, qtime in PBS
        * ctime in PBS
        * mean_power in PBS
        * mem_req in PBS
        * mpiprocs
        * ncpus_req in PBS, min_cpus, max_cpus in SLURM -> cpus
        * ngpus_req in PBS
        * nmics_req in PBS
        * nnodes_req in PBS, min_nodes, max_nodes, req_nodes, sched_nodes in SLURM -> nodes
        * project in PBS, SLURM part
        * qlist in PBS
        * core_list in SLURM, node_list in PBS -> node_list

    Same items:
        * job_id
        * user_id
        * start_time
        * end_time
        * account_name
        * job_name
    """
    def __init__(self,
                 job_id=-1,
                 user_id=-1,
                 start_time=None,
                 queue_time=None,
                 wait_time=-1,
                 end_time=None,
                 account_name='',
                 job_name='',
                 cpus=-1,
                 core_list=None,
                 nodes=-1,
                 node_list=None,
                 exit_code=-1,
                 active=False,
                 time=-1,
                 variables=[],
                 gpus=-1,
                 mpi_procs=-1,
                 mics=-1,
                 memory=-1,
                 project='',
                 ):
        self.log = logging.getLogger(__name__)

        self.job_id = job_id
        self.user_id = user_id
        self.start_time = start_time

        # Queue time doesn't have to present if wait_time is set
        if not queue_time and start_time and wait_time > -1:
            self.queue_time = start_time - timedelta(seconds=int(wait_time))
        elif queue_time:
            self.queue_time = queue_time
        else:
            self.log.warning("Queue time couldn't be set for job %s" % self.job_id)
            self.queue_time = queue_time

        self.end_time = end_time
        self.account_name = account_name
        self.job_name = job_name
        self.cpus = cpus
        self.core_list = core_list
        self.nodes = nodes
        self.node_list = node_list
        self.exit_code = exit_code
        self.active = active
        self.asoc_nodes = list()
        self.time = time
        self.variables = variables
        self.mpi_procs = mpi_procs
        self.mics = mics
        self.gpus = gpus
        self.memory = memory
        self.power = 0
        self.avg_temp = 0
        self.gpu_power = 0
        self.cpu_util = 0
        self.project = project

        try:
            self.associate_cores_nodes()
        except Exception as e:
            self.log.error(e)

    @classmethod
    def from_dict(cls, data):
        gpus = -1
        if 'ncpus_req' in data or 'nnodes_req' in data:
            # PBS Pro data
            cpus = data['ncpus_req']
            nodes = data['nnodes_req']
            gpus = data['ngpus_req']
            time = data.get('req_time')
            memory = data.get('req_mem')
            project = data.get('project_name')
            data['core_list'] = data['used_cores']
            data['node_list'] = data['used_nodes']
            data['queue_time'] = data['qtime']
        else:
            # SLURM data
            cpus = data['cpu_cnt']
            nodes = len(Job.split_list(data['node_list']))
            time = data['time_limit']
            memory = data['pn_min_memory']
            project = data['part']
            try:
                gpus = Job.split_list(data.get('gres_req'), delim=':')[1]
            except IndexError:
                pass

        return Job(job_id=data.get('job_id'),
                   user_id=data['user_id'],
                   start_time=data['start_time'],
                   queue_time=data.get('queue_time'),
                   wait_time=data.get('wait_time', -1),
                   end_time=data['end_time'],
                   account_name=data['account_name'],
                   job_name=data['job_name'],
                   cpus=cpus,
                   core_list=Job.split_list(data['core_list'], delim='#'),
                   nodes=nodes,
                   node_list=Job.split_list(data['node_list']),
                   exit_code=data.get('exit_code', -1),
                   time=time,
                   variables=data.get('var_list', []),
                   memory=memory,
                   project=project,
                   gpus=gpus,
                   mics=data.get('nmics_req', -1),
                   )

    def parse_node_list(self):
        pass

    @staticmethod
    def split_list(values, delim=','):
        """Remove all whitespaces and split by the delimiter"""
        return values.replace(' ', '').split(delim)

    @staticmethod
    def time_serializer(obj):
        """Default JSON serializer."""
        if isinstance(obj, datetime):
            if obj.utcoffset() is not None:
                obj = obj - obj.utcoffset()

            millis = int(calendar.timegm(obj.timetuple()) * 1000 + obj.microsecond / 1000)

            if obj.utcoffset() is None:
                millis -= (config['cassandradb'].getint('timezone_offset', 0) * 1000)
            return millis
        if isinstance(obj, decimal.Decimal):
            return float(obj)

        raise TypeError('Not sure how to serialize %s' % (obj,))

    def associate_cores_nodes(self):
        """Associate nodes with their cores.

        Expected format of cores: `core1, core2#core1#core1` where each core is separated
        by a comma and each node's core by a hash tag.

        Expected format of nodes: comma-separated list with the number of items as in cores
        list for nodes.
        """

        if len(self.node_list) != (len(self.core_list) - 1):
            # Both lists must have the same length
            raise Exception("Cores' and nodes' list lengths doesn't match!")

        for i in range(0, len(self.node_list)):
            self.asoc_nodes.append({
                "node": self.node_list[i],
                "cores": self.split_list(self.core_list[i])
            })

    @staticmethod
    def average(data):
        data = [float(x) for x in data]
        return sum(data)/float(len(data))

    def add_measures(self, data):
        self.power = self.average(self.split_list(data.get('power_mean'), delim='#')[:-1])
        self.gpu_power = self.average(self.split_list(data.get('gpu_power_mean'), delim='#')[:-1])
        self.cpu_util = self.average(self.split_list(data.get('util_p0_0_mean'), delim='#')[:-1])
        self.avg_temp = self.average(self.split_list(data.get('ambient_temp_mean'), delim='#')[:-1])

    def dict(self):
        return {
            'job_id': self.job_id,
            'user_id': self.user_id,
            'account_name': self.account_name,
            'job_name': self.job_name,
            'start_time': self.start_time,
            'queue_time': self.queue_time,
            'end_time': self.end_time,
            'cpus': self.cpus,
            'core_list': self.core_list,
            'nodes': self.nodes,
            'node_list': self.node_list,
            'exit_code': self.exit_code,
            'active': self.active,
            'asoc_nodes': self.asoc_nodes,
            'time': self.time,
            'variables': self.variables,
            'gpus': self.gpus,
            'mics': self.mics,
            'mpi_procs': self.mpi_procs,
            'power': self.power,
            'temp': self.avg_temp,
            'cpu_util': self.cpu_util,
            'gpu_power': self.gpu_power,
            'project': self.project,
        }

    def json(self):
        return json.dumps(self.dict(), default=Job.time_serializer)
