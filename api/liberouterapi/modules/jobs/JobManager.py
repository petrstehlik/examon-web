"""
PBS Job Manager class

This class manages all incoming messages regarding the PBS job info

Author:
    Petr Stehlik <xstehl14@stud.fit.vutbr.cz> @ 2017/07
"""

import paho.mqtt.client as mqtt
import logging, json, copy

class JobManager():

    # Callback function on what to do with the message before storing it in database
    on_receive = None

    # Database dictionary
    # Records are organized by the job ID and received message
    db = dict()

    db_fail = dict()

    finished = dict()

    def __init__(self,
            mqtt_broker,
            mqtt_port,
            mqtt_topics,
            drop_job_arrays = True,
            on_end = None):
        """
        drop_job_arrays The PBS hook sends job arrays where job ID is in format xxxxxxx[xxxx].io01
        """
        self.log = logging.getLogger(__name__)

        self.broker = mqtt_broker
        self.port = mqtt_port
        self.topics = [(str(topic), 0) for topic in mqtt_topics]

        self.drop_job_arrays = drop_job_arrays

        self.db = dict()
        self.db_fail = dict()

        self.client = mqtt.Client()

        # Register methods for connection and message receiving
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.on_receive = self.default_on_receive

        self.on_end = self.default_on_end

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
        self.log.info("Received message '%s': %s " % (msg.topic, json.dumps(msg.payload)))

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
            if jobid in self.db and "jobs_exc_begin" in self.db[jobid]:
                self.process_exc_end(jobid, payload)
            else:
                self.log.warn("Job '%s' - missing exc_begin or runjob event" % jobid)
                self.process_exc_end_fail(jobid, payload)

        # We received unknown message
        else:
            self.log.warn("Received unknown topic '%s'" % msg.topic)


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
        self.db[jobid]["exc_end"] = payload

        if "exc_end" in self.db[jobid]:
            self.db[jobid]["exc_end"].append(payload)
        else:
            self.db[jobid]["exc_end"] = [payload]

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
            self.db_fail[jobid] = self.db[jobid]
            del self.db[jobid]

        if "exc_begin" in self.db_fail[jobid]:
            self.db_fail[jobid]["exc_begin"].append(payload)
        else:
            self.db_fail[jobid]["exc_begin"] = [payload]

    def process_exc_end_fail(self, jobid, payload):
        if not jobid in self.db_fail:
            self.db_fail[jobid] = dict()

        # In case there is a previous correct event in the DB move it to failed
        if jobid in self.db:
            self.db_fail[jobid] = self.db[jobid]
            del self.db[jobid]

        if "exc_end" in self.db_fail[jobid]:
            self.db_fail[jobid]["exc_end"].append(payload)
        else:
            self.db_fail[jobid]["exc_end"] = [payload]

    def default_on_receive(self, jobid):
        pass

    def default_on_end(self, jobid):
        pass


