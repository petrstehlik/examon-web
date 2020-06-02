import os
import json
import requests

JOBARRAY = [
        "3390606.io01",
        "3390562.io01",
        "3389493.io01",
        "3408443.io01",
        "3419255.io01",
        "3414642.io01",
        "3414978.io01",
        "3394114.io01",
        "3390990.io01",
        "3384672.io01",
        "3394708.io01",
        "3394491.io01",
        "3394474.io01",
        "3394435.io01",
        "3394309.io01",
        "3394285.io01",
        "3394163.io01",
        "3394102.io01",
        "3393259.io01",
        "3392904.io01",
        "3390881.io01",
        "3389756.io01",
        "3389667.io01",
        "3389463.io01",
        "3419635.io01",
        "3419421.io01",
        "3403133.io01",
        "3410309.io01",
        "3409983.io01",
        "3409834.io01",
        "3418958.io01",
        "3394534.io01"
        ]

METRICS = [
    "AVX.ALL",
    "C2res",
    "C3res",
    "C6res",
    "CPU_Utilization",
    "IO_Utilization",
    "Mem_Utilization",
    "L1L2_bound",
    "L3_bound",
    "Sys_Utilization",
    "back_end_bound",
    "bad_speculation",
    "core_bound",
    "cpi",
    "freq",
    "front_end_bound",
    "ips",
    "load_core",
    "retiring",
]


def build_query(job, metric):
    return({
        'metrics': [{
            'name': metric,
            'aggregators': [{
                'align_sampling': True,
                'name': 'avg',
                'align_start_time': True,
                'sampling': {'unit': 'seconds', 'value': 30}
            }],
            'group_by': [{
                'name': 'tag',
                'tags': ['cluster']
            }],
            'tags': {
                'node': job["nodes"],
                'org': 'cineca',
                'cluster': 'galileo'
            }
        }],
        'end_absolute': (job["to"] - 7200) * 1000,
        'start_absolute': (job["from"] - 7200) * 1000
    })


def build_query_no_agg(job, metric):
    return({
        "start_absolute": (job["from"] - 7200) * 1000,
        "end_absolute": (job["to"] - 7200) * 1000,
        "metrics": [{
                "name": metric,
                "tags": {
                    "node": job["nodes"]
                },
                "group_by": [{
                    "name": "tag",
                    "tags": ["node"]
                }]
            }]
    })


def get_job(job):
    try:
        os.makedirs("../data_new/" + job['job_id'])
    except Exception as e:
        print("{}: Folder exists, skipping".format(job['job_id']))
        return

    for metric in METRICS:
        print("Job %s: fetching %s" % (job['job_id'], metric))
        # Fetch every metric and dump to file in ../data/<job_id>.json
        #r = requests.post("http://137.204.213.218:8083/api/v1/datapoints/query",
        #        data=json.dumps(build_query(job, metric)),
        #        auth=('galileo', 'g4l1l30975'))
        r2 = requests.post("http://137.204.213.218:8083/api/v1/datapoints/query",
                data=json.dumps(build_query_no_agg(job, metric)),
                auth=('galileo', 'g4l1l30975'))

        #with open("../data/" + job["job_id"] + "/" + metric + ".json", "w+") as fh:
        #    fh.write(r.text)

        res = r2.json()

        try:
            if res['queries'][0]['sample_size'] > 0:
                with open("../data_new/" + job["job_id"] + "/" + metric + "_raw.json", "w+") as fh:
                    fh.write(r2.text)
        except Exception as e:
            print(e)
            print(r2.text)


if __name__ == "__main__":
    jobs = None
    good_jobs = []

    with open("target_jobs_1523524915.json") as fh:
        jobs = json.load(fh)

    for job in jobs:
        if job['to'] - job['from'] >= 300 and job['cpus_req'] % 16 == 0:
            good_jobs.append(job['job_id'])
            #get_job(job)

    print(len(good_jobs))


    """for item in jobs:
        if item["job_id"] in JOBARRAY:
            #if item["job_id"] == "3394534.io01":
            #item["job_id"] = "0.io01"
            get_job(item)
            print("Job %s fetched" % item["job_id"])
    """

