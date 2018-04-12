import numpy as np
import scipy.interpolate as interp
import json
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

metrics = [
    "load_core",
    "Sys_Utilization",
    "IO_Utilization",
    "Mem_Utilization",
    "CPU_Utilization",
    "L1L2_Bound",
    "L3_Bound",
    "ips",
    "front_end_bound",
    "back_end_bound",
    "C3res",
    "C6res",
    #"job_CPU1_Temp",
    #"job_CPU2_Temp"
        ]


def stretch(data, size=120, transform=True):
    """
    Take datapoints and stretch them to (60*60*24)/30 = 2880 values using interpolation
    """
    points = np.array(data)

    if transform:
        points = np.array([point[1] for point in data])

    interp_points = interp.interp1d(np.arange(points.size), points)
    stretched = interp_points(np.linspace(0, points.size - 1, size))

    return stretched.tolist()


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

