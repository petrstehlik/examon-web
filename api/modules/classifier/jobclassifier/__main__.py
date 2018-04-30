import logging
import sys
import json
import numpy as np
from multiprocessing import Pool
import argparse
import os
import signal
import sqlite3

from network import Network
from neuron import Neuron
import analyzer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("MAIN")
metric_data = dict()
networks = list()
args = dict()


class NetworkList(object):
    C6 = 0
    C3 = 1
    load_core = 2
    ips = 3
    sys_util = 4
    io_util = 5
    mem_util = 6
    cpu_util = 7
    l1l2_bound = 8
    l3_bound = 9
    front_end_bound = 10
    back_end_bound = 11


metrics = [
        "C6res",
        "C3res",
        "load_core",
        "ips",
        "Sys_Utilization",
        "IO_Utilization",
        "Mem_Utilization",
        "CPU_Utilization",
        "L1L2_bound",
        "L3_bound",
        "front_end_bound",
        "back_end_bound",
        "jobber"
        ]


INPUTS = 80
DATA = []


def load_data():
    global metrics
    # jobs = os.listdir('../../../../../examon-data/data_cluster')
    conn = sqlite3.connect('../../../database-galileo.sq3')
    conn.row_factory = sqlite3.Row

    jobs = conn.cursor().execute('SELECT job_id FROM classifier').fetchall()

    for job in jobs:
        job_data = {
            'jobber': {
                'data': []
            }
        }
        job_id = job[0]

        susp = conn.cursor().execute('SELECT * FROM classifier WHERE job_id="{}"'.format(job_id)).fetchone()
        for m in metrics[:-1]:
            with open(os.path.join('../../../../../examon-data/data_cluster', job_id, m + '_raw.json')) as f:
                m_data = json.load(f)
                job_data[m] = {
                    'data': analyzer.stretch(m_data['queries'][0]['results'][0]['values'], size=INPUTS),
                    'suspicious': [susp[m]]
                }
            job_data['jobber']['data'].append(susp[m])
        job_data['jobber']['suspicious'] = [susp['jobber']]

        DATA.append(normalize(job_data))


def normalize(job):
    global metrics
    for metric in metrics[:-1]:
        if metric == "ips":
            job[metric]['data'] = map(lambda x: x / 8000000000.0, job[metric]['data'])
        elif metric == 'back_end_bound':
            if job[metric]['data'][0] > 110:
                job[metric]['data'] = map(lambda x: x / 10000000.0, job[metric]['data'])
            else:
                job[metric]['data'] = map(lambda x: x / 100.0, job[metric]['data'])
        else:
            # normalize to fraction percentage
            job[metric]['data'] = map(lambda x: x / 100.0, job[metric]['data'])
    return job


def runner(x):
    """Train a network using given metric.

    :param x: metric name
    """
    global metrics
    global args

    try:
        networks[x].train(metric_data[metrics[x]][:250], 0.5, epochs=args.epochs, epsilon=0.1)
    except Exception as e:
        log.error("Exception: {}, dumping config for {}".format(str(e), metrics[x]))
    with open(os.path.join(args.config_dir, metrics[x] + '_network.json'), 'w+') as fp:
        json.dump(networks[x].export(), fp)


def arg_parser():
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
    pass
    # signal.signal(signal.SIGINT, signal.SIG_IGN)


if __name__ == "__main__":
    arg_parser()
    log.info("Loading data")
    load_data()

    # Reorganize data so that metrics from jobs are together
    for metric in metrics:
        # Prepare metric data
        metric_data[metric] = []
        for job in DATA:
            md = job[metric]['data']
            md.append(job[metric]['suspicious'])
            metric_data[metric].append(md)

    log.info('Data ready')

    if args.train:
        # Create folder for networks configurations
        try:
            os.makedirs(args.config_dir)
        except Exception as e:
            log.info("Folder exists, overwriting existing configurations")
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
            p = Pool(processes=13, initializer=initializer)

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
                print("Expected: {0}, Got: {1:.2f}".format(item[-1], (network.predict(item[:-1])[0])))

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

