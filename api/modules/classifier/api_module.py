import json
import os
import requests

from muapi import app
from jobclassifier.analyzer import metrics, stretch
from jobclassifier.network import Network

from modules.models.Job import Job
from modules.jobs.cassandra_connector import connect, prepare_statements

import logging

log = logging.getLogger(__name__)


try:
    session = connect()
    prepared = prepare_statements(session)
except Exception as e:
    log.error("Failed to connect to Cassandra: %s" % str(e))


def get_job(jobid):
    log.info("Query for job ID", jobid)

    try:
        jobid = int(jobid)
    except ValueError:
        pass

    info = session.execute(prepared["sel_by_job_id"], (jobid,))
    if len(info.current_rows) == 0:
        return '', 404

    job = Job.from_dict(info[0])

    # Try to fetch measurements from DB
    measures = session.execute(prepared["measures"], (jobid,))

    if len(measures.current_rows) > 0:
        job.add_measures(measures[0])

    return job

def initialize_networks():
    output_networks = {}
    for x, metric in enumerate(metrics):
        with open(os.path.join(os.path.dirname(__file__), 'configs/{}_network.json'.format(metric))) as fp:
            output_networks[metric] = Network.load(json.load(fp))

    return output_networks


def build_query_no_agg(job, metric):
    return {
        "start_absolute": Job.time_serializer(job.start_time),
        "end_absolute": Job.time_serializer(job.end_time),
        "metrics": [{
                "name": metric,
                "tags": {
                    "node": job.node_list
                },
                "group_by": [{
                    "name": "tag",
                    "tags": ["cluster"]
                }]
            }]
    }


def get_job_data(job):
    data = {}
    for metric in metrics:
        print("Job %s: fetching %s" % (job.job_id, metric))
        query = build_query_no_agg(job, metric)
        # Fetch every metric and dump to file in ../data/<job_id>.json
        r = requests.post("http://137.204.213.218:8083/api/v1/datapoints/query",
                data=json.dumps(query),
                auth=('galileo', 'g4l1l30975'))

        data[metric] = r.json()

        data[metric] = data[metric]['queries'][0]['results'][0]['values']

    return data


def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in xrange(0, len(l), n))


def normalize(job):
    for metric in metrics:
        if metric == "job_ips":
            for point in job[metric]:
                point[1] = point[1]/(8000000000.0)
        if metric == "job_CPU1_Temp" or metric == "job_CPU2_Temp":
            # Skip temperatures
            continue
        else:
            for point in job[metric]:
                # normalize to fraction percentage
                point[1] = point[1]/100.0
    return job


networks = initialize_networks()


@app.route('/classifier/<string:job_id>')
def classify(job_id):
    """Classify a job by its job ID"""
    global networks

    # Fetch job info
    job = get_job(job_id)

    # Fetch job data based on job info
    job_data = normalize(get_job_data(job))

    metric_data = {}

    res = {}

    for m in metrics:
        try:
            data = stretch(job_data[m], len(job_data[m]))

            res[m] = []

            for chunk in chunks(data, 120):
                data = stretch(chunk, transform=False)
                res[m].append(networks[m].predict(data))
        except:
            pass

    # Normalize the dataset

    # Classify the job
    return json.dumps(res)
