"""
PBS Job Manager class

This class manages all incoming messages regarding the PBS job info

Author:
    Petr Stehlik <xstehl14@stud.fit.vutbr.cz> @ 2017/07
"""

from __future__ import print_function
import paho.mqtt.client as mqtt
import logging, json, copy
import time

from muapi import config

class JobManager():

    # Callback function on what to do with the message before storing it in database
    on_receive = None

    # Database dictionary
    # Records are organized by the job ID and received message
    db = dict()

    db_fail = dict()

    finished = dict()

    def __init__(self, mqtt_broker, mqtt_port, mqtt_topics):
        """
        drop_job_arrays The PBS hook sends job arrays where job ID is in format xxxxxxx[xxxx].io01
        """
        self.log = logging.getLogger(__name__)

        self.broker = mqtt_broker
        self.port = mqtt_port
        self.topics = [(str(topic), 0) for topic in mqtt_topics]

        self.db = dict()
        self.db_fail = dict()

        self.client = mqtt.Client()

        # Register methods for connection and message receiving
        self.client.on_connect = self.on_connect
        self.client.on_message = self.process

        self.on_receive = self.default_on_receive

        self.on_end = self.default_on_end
        self.on_fail = self.default_on_fail

        self.system_nnodes = config['SINFO'].getint('system_nnodes')
        self.system_cores_per_node = config['SINFO'].getint('system_cores_per_node')
        self.client.connect(mqtt_broker, self.port, 60)

        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """
        Subscribe to all topics
        """
        result, mid = client.subscribe(self.topics)

        if result == mqtt.MQTT_ERR_SUCCESS:
            self.log.info("Successfully subscribed to all topics")
        else:
            self.log.error("Failed to subscribe to topics")

    def on_message(self, client, userdata, msg):
        """
        Take action on received messages
        Currently parsed actions:
            jobs_runjob
            jobs_exc_begin
            jobs_exc_end
        """
        self.log.info("Received message '%s': %s " % (msg.topic, msg.payload))

        topic = str(msg.topic).split('/')

        try:
            payload = json.loads(str(msg.payload).replace("'", '"'))
        except Exception as e:
            self.log.error("Failed to load JSON payload. Reason: %s" % str(e))
            return

        jobid = str(payload['job_id'])

        # Process runjob event
        if topic[-1] == "jobs_runjob":
            self.process_runjob(jobid, payload)
            return

        # Process exc_begin event
        # This event requires the runjob event to be already present in the DB
        elif topic[-1] == "jobs_exc_begin":
            if jobid in self.db:
                self.process_exc_begin(jobid, payload)
            else:
                self.log.warn("Job '%s' - missing runjob event" % jobid)
                self.process_exc_begin_fail(jobid, payload)

        # Process end event of job exec
        elif topic[-1] == "jobs_exc_end":
            if (
                    jobid in self.db and
                    "exc_begin" in self.db[jobid] and
                    len(self.db[jobid]["exc_begin"]) == len(payload["vnode_list"])
            ):
                self.process_exc_end(jobid, payload)
            else:
                self.log.warn("Job '%s' - missing exc_begin or runjob event" % jobid)
                self.process_exc_end_fail(jobid, payload)

        # We received unknown message
        else:
            self.log.warn("Received unknown topic '%s'" % msg.topic)
            return

        self.check_timeout()

    def process_runjob(self, jobid, payload):
        """
        Process runjob message

        Example payload: {
            project":"_pbs_project_default",
            "vnode_list":["node215"],
            "job_id":"2901535.io01",
            "ngpus":0,
            "qtime":1502446511,
            "req_mem":"8192",
            "node_list":["None"],
            "job_name":"STDIN",
            "queue":"shared",
            "req_cpus":1,
            "nmics":0,
            "req_time":1800,
            "variable_list ":{
                "PBS_O_SYSTEM":"Linux",
                "PBS_O_SHELL":"/bin/bash"
            },
            "job_owner":"pstehlik",
            "backup_qtime":"2017-08-11 12:15:35",
            "mpiprocs":1,
            "Qlist":"cincomp",
            "account_name":"PHD_Summer17_1",
            "ctime":1502446511
        }

        Notes:
            qtime - UNIX timestamp
            backup_qtime - ISO timestamp
            ctime - UNIX timestamp
        """
        if jobid in self.db:
            # The job is already there
            self.db[jobid]["runjob"].append(payload)
        else:
            self.db[jobid] = {
                    "runjob" : [payload]
                }

        self.on_receive(jobid)

    def process_exc_begin(self, jobid, payload):
        """
        Example payload: "org/cineca/cluster/galileo/jobs_exc_begin":{
            "vnode_list":["node064"],
            "job_id":"2901321.io01",
            "job_cores":[0,1],
            "start_time":"2017-08-11 11:19:09",
            "node_list":[
            "node064"
            ],
            "node_id":"node064",
            "job_owner":"pstehlik",
            "job_name":"STDIN"
        }
        """
        if "exc_begin" in self.db[jobid]:
            self.db[jobid]["exc_begin"].append(payload)
        else:
            self.db[jobid]["exc_begin"] = [payload]

        self.on_receive(jobid)

    def process_exc_end(self, jobid, payload):
        """
        {
            "vnode_list":["node063"],
            "cpupercent":0,
            "job_id":"2901306.io01",
            "job_cores":[0,1],
            "used_vmem":"3",
            "cputime":0,
            "used_mem":"3",
            "node_id":"node063",
            "end_time":"2017-08-11 11:11:31",
            "node_list":["node063"],
            "job_owner":"pstehlik",
            "job_name":"STDIN",
            "real_walltime":41
        }
        """
        if "exc_end" in self.db[jobid]:
            self.db[jobid]["exc_end"].append(payload)
        else:
            self.db[jobid]["exc_end"] = [payload]

        # Check if all "exc_end" messages are in the DB
        # if everything is in place we can trigger the on_end method and remove it from active
        self.on_receive(jobid)

        if len(self.db[jobid]["exc_end"]) == len(self.db[jobid]["exc_end"][0]["vnode_list"]):
            self.on_end(jobid)

            # All is done, remove the job from DB
            self.log.info("Removing job %s from DB" % jobid)

            # DEVEL only to see finished jobs
            self.finished[jobid] = copy.deepcopy(self.db[jobid])

            del self.db[jobid]

    def process_exc_begin_fail(self, jobid, payload):
        if jobid not in self.db_fail:
            self.db_fail[jobid] = dict()

        # In case there is a previous correct event in the DB move it to failed
        if jobid in self.db:
            self.db_fail[jobid] = copy.deepcopy(self.db[jobid])
            del self.db[jobid]

        if "exc_begin" in self.db_fail[jobid]:
            self.db_fail[jobid]["exc_begin"].append(payload)
        else:
            self.db_fail[jobid]["exc_begin"] = [payload]

        self.on_fail(jobid)

    def process_exc_end_fail(self, jobid, payload):
        if not jobid in self.db_fail:
            self.db_fail[jobid] = dict()

        # In case there is a previous correct event in the DB move it to failed
        if jobid in self.db:
            self.db_fail[jobid] = copy.deepcopy(self.db[jobid])
            del self.db[jobid]

        if "exc_end" in self.db_fail[jobid]:
            self.db_fail[jobid]["exc_end"].append(payload)
        else:
            self.db_fail[jobid]["exc_end"] = [payload]

        self.on_fail(jobid)

    def check_timeout(self):
        """Check timeout in all active records
        The timeout time is taken as ctime + req_time and compared to current unix timestamp
        If current timestamp is smaller, the job is moved to failed db
        """
        for jobid in self.db.copy():
            timeout = self.db[jobid]['runjob'][0]['ctime'] + self.db[jobid]['runjob'][0]['req_time']
            now = int(time.time())

            if timeout < now:
                self.db_fail[jobid] = copy.deepcopy(self.db[jobid])
                del self.db[jobid]
                self.log.info("TIMEOUT: Moving job %s to fail DB" % jobid)
                self.on_fail(jobid)

    def default_on_receive(self, jobid):
        pass

    def default_on_end(self, jobid):
        pass

    def default_on_fail(self, jobid):
        pass

    def process(self, client, user_data, msg):
        """Process MQTT message from SLURM-based system."""

        job_info = msg.payload.split(';')

        # as alternative solution: count with normal indexes up to the var list
        # (0-16); then, the remaining fields are computed as
        # len(job_info) - 1 - alternative_index

        data = dict(
            job_id=int(job_info[0].strip()),
            part=job_info[1].strip(),
            user_id=int(job_info[2].strip()) or "None",
            job_name=job_info[3].strip(),
            account_name=job_info[4].strip(),
            nodes=job_info[5].strip(),
            exc_nodes=job_info[6].strip(),
            sched_nodes=job_info[7].strip(),
            req_nodes=job_info[8].strip(),
            node_count=int(job_info[11].strip()),
            time_limit=int(job_info[12].strip()),
            gres_req=job_info[13].strip(),
            cpu_cnt=int(job_info[14].strip()),
            exit_code=int(job_info[15].strip()),
            elapsed_time=float(job_info[16].strip()),
            wait_time=float(job_info[17].strip()),
            num_task=int(job_info[18].strip()),
            num_task_perNode=int(job_info[19].strip()),
            cpus_perTask=int(job_info[20].strip()),
            contiguous=int(job_info[21].strip()),
            licence=job_info[22].strip(),
            dependency=job_info[23].strip(),
            features=job_info[24].strip(),
            overcommit=int(job_info[25].strip()),
            pn_min_memory=int(job_info[26].strip()),
            pn_min_tmp_disk=int(job_info[27].strip()),
            share_res=int(job_info[28].strip()),
            task_dist=int(job_info[29].strip()),
            max_nodes=int(job_info[30].strip()),
            min_nodes=int(job_info[31].strip()),
            max_cpus=int(job_info[32].strip()),
            min_cpus=int(job_info[33].strip()),
            begin_time=job_info[34].strip(),
            submit_time=job_info[35].strip(),
            start_time=job_info[36].strip(),
            end_time=job_info[37].strip(),
        )

        if(job_info[9].strip() == "None" or
                job_info[9].strip() == "(null)"):
            logging.warning("Problem with node bitmap")
            # if there was a problem with node_bitmap we can try to
            # retrieve used nodes from other fields (but it's actually
            # not needed since all other script just use 'nodes' field
            node_bitmap = "None"
            node_list = "-1"
        else:
            node_bitmap = job_info[9].strip()
            node_list = ""
            node_bitmap_split = node_bitmap.split(',')
            if len(node_bitmap_split) <= 1:
                node_first = int(node_bitmap.split('-')[0])
                if len(node_bitmap.split('-')) > 1:
                    node_last = int(node_bitmap.split('-')[1])
                else:
                    node_last = node_first
                for i in range(node_first, node_last+1):
                    node_list += str(node_first + i) + ','
            else:
                for nb in node_bitmap_split:
                    node_first = int(nb.split('-')[0])
                    if len(nb.split('-')) > 1:
                        node_last = int(nb.split('-')[1])
                    else:
                        node_last = node_first
                    for i in range(node_first, node_last+1):
                        node_list += str(node_first + i) + ','
            data['node_list'] = node_list[:-1]
            data['node_bitmap'] = node_bitmap

        if(job_info[10].strip() == "None" or
                job_info[10].strip() == "(null)"):
            print("Problem with core bitmap")
            logging.warning("Problem with core bitmap")
            # if there was a problem with core_bitmap we cannot retrieve
            # used cores in another way
            core_bitmap = "None"
            core_list = "-1"
        else:
            core_bitmap = job_info[10].strip()
            core_list = ""
            core_bitmap_split = core_bitmap.split(',')
            if len(core_bitmap_split) <= 1:
                core_first = int(core_bitmap.split('-')[0])
                if len(core_bitmap.split('-')) > 1:
                    core_last = int(core_bitmap.split('-')[1])
                else:
                    core_last = core_first
                cores_on_node = {}
                for i in range(core_first, core_last+1):
                    index = (core_first + i) // self.system_nnodes
                    if index in cores_on_node:
                        cores_on_node[index].append(
                                        (core_first + i) %
                                        self.system_cores_per_node)
                    else:
                        cores_on_node[index] = [
                                        (core_first + i) %
                                        self.system_cores_per_node]
                for key, vals in cores_on_node.iteritems():
                    core_list += str(vals)[1:-1] + '# '
            else:
                for cb in core_bitmap_split:
                    core_first = int(cb.split('-')[0])
                    if len(cb.split('-')) > 1:
                        core_last = int(cb.split('-')[1])
                    else:
                        core_last = core_first
                    cores_on_node = {}
                    for i in range(core_first, core_last+1):
                        index = (core_first + i) // self.system_nnodes
                        if index in cores_on_node:
                            cores_on_node[index].append(
                                            (core_first + i) %
                                            self.system_cores_per_node)
                        else:
                            cores_on_node[index] = [
                                            (core_first + i) %
                                            self.system_cores_per_node]
                    for key, vals in cores_on_node.iteritems():
                        core_list += str(vals)[1:-1] + '# '
        data['core_list'] = core_list
        data['node_bitmap'] = node_bitmap
        data['core_bitmap'] = core_bitmap
        data['node_list'] = node_list

        for key in data.keys():
            # Clear null values
            if data[key] == '(null)':
                data[key] = None

        self.db[data['job_id']] = data
