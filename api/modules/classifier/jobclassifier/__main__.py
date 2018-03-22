import logging
import sys
import json
import numpy as np
from multiprocessing import Pool
import argparse
import os
import signal

from network import Network
from neuron import Neuron
import analyzer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("MAIN")
metric_data = dict()
networks = list()
args = dict()

class NetworkList:
    C6              = 0
    C3              = 1
    load_core       = 2
    ips             = 3
    sys_util        = 4
    io_util         = 5
    mem_util        = 6
    cpu_util        = 7
    l1l2_bound      = 8
    l3_bound        = 9
    front_end_bound = 10
    back_end_bound  = 11

metrics = [
        "job_C6res",
        "job_C3res",
        "job_load_core",
        "job_ips",
        "job_Sys_Utilization",
        "job_IO_Utilization",
        "job_Mem_Utilization",
        "job_CPU_Utilization",
        "job_L1L2_Bound",
        "job_L3_Bound",
        "job_front_end_bound",
        "job_back_end_bound",
        "jobber"
        ]


INPUTS = 80

def normalize(job):
    for metric in analyzer.metrics:
        if metric == "job_ips":
            for point in job[metric]['data']:
                point[1] = point[1]/(8000000000.0)
        if metric == "job_CPU1_Temp" or metric == "job_CPU2_Temp":
            # Skip temperatures
            continue
        else:
            for point in job[metric]['data']:
                # normalize to fraction percentage
                point[1] = point[1]/(100.0)
    return job

def runner(x):
    global metrics
    global args

    try:
        networks[x].train(metric_data[metrics[x]], 0.5, epochs = args.epochs, epsilon = 0.1)
    except Exception as e:
        log.error("Exception: {}, dumping config for {}".format(str(e), metrics[x]))
    with open(os.path.join(args.config_dir, metrics[x] + '_network.json'), 'w+') as fp:
        json.dump(networks[x].export(), fp)

def argparser():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--train',
            action="store_true",
            help='Train the network using data.json dataset')
    parser.add_argument('--eval',
            dest='config_eval',
            default='configs',
            help='Evaluate learned network with data.json dataset')
    parser.add_argument('--dir',
            dest='config_dir',
            default='configs',
            help='Where to store configs')
    parser.add_argument('--max-epochs',
            dest="epochs",
            type=int,
            help="Maximum number of epochs (default: 10 000)",
            default=10000)

    args = parser.parse_args()

def initializer():
    """Ignore CTRL+C in the worker process."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__ == "__main__":
    argparser()
    log.info("Loading data")
    with open('data.json') as fp:
        data = json.load(fp)

    log.info("Normalizing dataset")
    for job in data:
        job = normalize(job)

    # Reorganize and interpolate data so that metrics from jobs are together
    metric_data["jobber"] = []
    for metric in metrics[:-1]:
        metric_data[metric] = []
        for job in data:
            # Prepare metric data
            point_data = analyzer.stretch(job[metric]['data'], size = INPUTS)
            point_data = point_data.tolist()
            point_data.append([1 if job[metric]['suspicious'] else 0])
            metric_data[metric].append(point_data)

    for job in data:
        # Prepare jobber data
        record = [1 if job[m]['suspicious'] else 0 for m in metrics[:-1]]
        record.append([1 if job['suspicious'] else 0])

        metric_data["jobber"].append(record)


    if args.train:
        # Create folder for networks configurations
        try:
            os.makedirs(args.config_dir)
        except Exception as e:
            log.info("Folder exists, overwriting existings configurations")
        networks = [
                Network([INPUTS, INPUTS/20, 3, 1], "C6res"),
                Network([INPUTS, INPUTS/20, 3, 1], "C3res"),
                Network([INPUTS, INPUTS/20, 3, 1], "load_core"),
                Network([INPUTS, INPUTS/20, 3, 1], "ips"),
                Network([INPUTS, INPUTS/20, 3, 1], "Sys_Utilization"),
                Network([INPUTS, INPUTS/20, 3, 1], "IO_Utilization"),
                Network([INPUTS, INPUTS/20, 3, 1], "Mem_Utilization"),
                Network([INPUTS, INPUTS/20, 3, 1], "CPU_Utilization"),
                Network([INPUTS, INPUTS/20, 3, 1], "L1L2_Bound"),
                Network([INPUTS, INPUTS/20, 3, 1], "L3_Bound"),
                Network([INPUTS, INPUTS/20, 3, 1], "front_end_bound"),
                Network([INPUTS, INPUTS/20, 3, 1], "back_end_bound"),
                Network([12, 4, 1], "jobber")
                ]

        log.info("Starting training")

        try:
            p = Pool(processes = 13, initializer=initializer)

            p.map(runner, range(13))
            p.close()
        except KeyboardInterrupt as e:
            print(e)
            p.terminate()
        p.join()

    else:
        network = None

        for x, metric in enumerate(metrics):
            with open(os.path.join(args.config_eval, metric + '_network.json'),) as fp:
                network = Network.load(json.load(fp))

            print("-- {}".format(metric))
            for item in metric_data[metric][-5:]:
                print("Expected: {0}, Got: {1:.2f}"
                        .format(item[-1], (network.predict(item[:-1])[0])))

        print("Complex Job Evaluating")
        networks = [None] * (len(metrics))
        for x, metric in enumerate(metrics):
            with open(os.path.join(args.config_eval, metric + '_network.json'),) as fp:
                networks[x] = Network.load(json.load(fp))

        for i in range(5):
            job = []
            j = len(metric_data[metrics[x]]) - 5 + i
            for x, network in enumerate(networks[:-1]):
                job.append(network.predict(metric_data[metrics[x]][j][:-1])[0])

            res = networks[-1].predict(job)
            print("Expected: {1}, Got: {0:.2f}".format(res[0], metric_data['jobber'][j][-1][0]))

