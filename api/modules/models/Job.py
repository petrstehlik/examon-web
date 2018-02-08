import logging
import calendar
from datetime import datetime, timedelta
import decimal
import json

from muapi import config

import pdb


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
        * project in PBS
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

    @classmethod
    def from_dict(cls, data):
        if 'ncpus_req' in data:
            # PBS Pro data
            cpus = data['ncpus_req']
        else:
            # SLURM data
            cpus = data['min_cpus']

        if 'nnodes_req' in data:
            # PBS Pro data
            nodes = data['nnodes_req']
        else:
            # SLURM data
            nodes = data['min_nodes']

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

    def json(self):
        return json.dumps({
            'job_id': self.job_id,
            'user_id': self.user_id,
            'account_name': self.account_name,
            'job_name': self.account_name,
            'start_time': self.start_time,
            'queue_time': self.queue_time,
            'end_time': self.end_time,
            'cpus': self.cpus,
            'core_list': self.core_list,
            'nodes': self.nodes,
            'node_list': self.node_list,
            'exit_code': self.exit_code,
            'active': self.active,
        }, default=Job.time_serializer)