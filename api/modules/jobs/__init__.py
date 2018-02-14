from muapi import config
from muapi.error import ApiException
from modules.utils import transform_live_job, time_serializer, split_list
from modules.models.Job import Job

from flask import request
from muapi.Module import Module
from .JobManager import JobManager

from .cassandra_connector import connect, prepare_statements
import json
import datetime, time, calendar
import logging


jobman = JobManager(config['jobs']['server'], 1883, json.loads(config['jobs']['topics']))

from .sockets import *

jobman.on_receive = emit_data

log = logging.getLogger(__name__)


class JobsError(ApiException):
    status_code = 500


try:
    session = connect()
    prepared = prepare_statements(session)
except Exception as e:
    log.error("Failed to connect to Cassandra: %s" % str(e))

jobs = Module('jobs', __name__, url_prefix = '/jobs', no_version=True)


@jobs.route('/<string:jobid>', methods=['GET'])
def jobs_hello(jobid):
    log.info("Query for job ID", jobid)

    if jobid in jobman.db:
        # The job is currently running, we can fetch the info we need
        return json.dumps(transform_live_job(jobid, jobman), default=Job.time_serializer)

    info = session.execute(prepared["sel_by_job_id"], (int(jobid),))
    if len(info.current_rows) == 0:
        return '', 404

    job = Job.from_dict(info[0])

    # Try to fetch measurements from DB
    measures = session.execute(prepared["measures"], (int(jobid),))

    if len(measures.current_rows) > 0:
        job.add_measures(measures[0])

    return job.json()

@jobs.route('/latest')
def jobs_latest():
    """
        Fetch all jobs that finished in last 30 minutes,
        sort them by start_time and return the last one.
    """

    # Get last job ID
    last_job = session.execute("select max(job_id) as job_id from davide_jobs_simplekey")
    qres = session.execute("SELECT * FROM davide_jobs_simplekey \
            WHERE job_id = {}".format(last_job[0]['job_id']))

    if len(qres.current_rows) == 0:
        # No jobs finished in last 30 minutes, try 12 hours
        tstamp = (int(time.time()) - 43200) * 1000
        qres = session.execute("SELECT * FROM davide_jobs_simplekey \
            WHERE  start_time >= " \
            + str(tstamp) + " ALLOW FILTERING")

    results = [item for item in qres]

    ordered = sorted(results, key = lambda k : k['end_time'])
    return json.dumps(ordered[-1], default=time_serializer)


@jobs.route('/stats/total', methods=['GET'])
def jobs_total():
    """
        Analyze jobs in given period

        GET params:
            from (required) UNIX timestamp in milliseconds
            to (optional) UNIX timestamp in milliseconds
    """
    args = request.args.to_dict()

    if "from" in args:
        # Convert to int so we can compare it
        args["from"] = int(args["from"])
    else:
        raise JobsError("Missing 'from' in GET parameters")

    if "to" not in args:
        # Generate timestamp
        args["to"] = int(time.time()) * 1000

    if args["to"] < args["from"]:
        raise JobsError("'from' time cannot precede 'to' time")

    qres = session.execute("SELECT job_id, nnodes_req, ncpus_req, ngpus_req, nmics_req, start_time, end_time \
        FROM davide_jobs_simplekey \
        WHERE token(user_id) > token('') AND \
            start_time >= " + str(args["from"]) + " AND \
            start_time <= " + str(args["to"]) + " ALLOW FILTERING")

    results = {
            "duration" : 0,
            "nodes" : 0,
            "cpus" : 0,
            "gpus" : 0,
            "mics" : 0,
            "from" : args["from"],
            "to" : args["to"],
            "jobs" : len(qres.current_rows)
        }

    for item in qres:
        results["duration"] += get_duration(item["start_time"], item["end_time"]) * item["ncpus_req"]
        results["nodes"] += item["nnodes_req"]
        results["cpus"] += item["ncpus_req"]
        results["gpus"] += item["ngpus_req"]
        results["mics"] += item["nmics_req"]

    return(json.dumps(results))

@jobs.route('/active', methods=['GET'])
def get_active_jobs():
    return(json.dumps(jobman.db))

@jobs.route('/failed', methods=['GET'])
def get_failed_jobs():
    return(json.dumps(jobman.db_fail))

@jobs.route('/finished', methods=['GET'])
def get_finished_jobs():
    return(json.dumps(jobman.finished))
