import numpy as np
import scipy.interpolate as interp
import json
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

metrics = [
    "job_load_core",
    "job_Sys_Utilization",
    "job_IO_Utilization",
    "job_Mem_Utilization",
    "job_CPU_Utilization",
    "job_L1L2_Bound",
    "job_L3_Bound",
    "job_ips",
    "job_front_end_bound",
    "job_back_end_bound",
    "job_C3res",
    "job_C6res",
    "job_CPU1_Temp",
    "job_CPU2_Temp"
        ]

def stretch(data, size = 120):
    """
    Take datapoints and stretch them to (60*60*24)/30 = 2880 values using interpolation
    """
    points = np.array([point[1] for point in data])
    interp_points = interp.interp1d(np.arange(points.size), points)
    stretched = interp_points(np.linspace(0, points.size - 1, size))

    #log.debug(points)
    #log.debug(stretched)
    return(stretched)

def stats(data):
    """
    output to logging basic statistical information
    """
    susp = 0
    metr = 0
    datapoints = 0

    for job in data:
        if job['suspicious']:
            susp += 1

            for metric in metrics:
                datapoints += len(job[metric]['data'])
                if job[metric]['suspicious']:
                    metr += 1

    log.info("{}/{} jobs suspicious".format(susp, len(data)))
    log.info("{}/{} job metrics suspicious".format(metr, len(data) * len(metrics)))
    log.info("{} datapoints".format(datapoints))

if __name__ == "__main__":
    with open('../data.json') as fp:
        data = json.load(fp)

    stats(data)

    stretch(data[-1][metrics[-1]]['data'])

