from collections import OrderedDict

from muapi import config, app
from .error import JobsError
from .Aggregate import Aggregate

from flask import request
from pyKairosDB import connect, reader
import json
import requests
import os


conn = connect(server=config["kairosdb"].get("server", "localhost"),
               port=config["kairosdb"].get("port", 8000),
               user=config["kairosdb"].get("user", ""),
               passw=config["kairosdb"].get("password", "")
               )

from .utils import check_times, generate_health_url, generate_base_url, extract_data, merge_dicts, join_data


def load_data(job_id, metric, grouper='node'):
    with open(os.path.join(config['data']['path'], job_id, metric + '_raw.json')) as f:
        res = json.load(f)
        labels = list()
        data = OrderedDict()

        extract_data(res, data, labels, [grouper])

        return ({
            "points": data,
            "labels": labels,
            "metric": metric
        })


@app.route("/kairos/health")
def health():
    res = requests.get(generate_health_url() + "/check", auth=(conn.user, conn.passw))
    return '', res.status_code


@app.route("/kairos/status")
def status():
    res = requests.get(generate_health_url() + "/status", auth=(conn.user, conn.passw))
    return str(res.content)


@app.route("/kairos/metrics")
def list_metrics():
    """
    List all available metrics
    """
    res = requests.get(generate_base_url() + "/metricnames", auth=(conn.user, conn.passw))
    return str(res.content)


@app.route("/kairos/tags")
def list_tags():
    """
    List all available metrics
    """
    res = requests.get(generate_base_url() + "/tagnames", auth=(conn.user, conn.passw))
    return str(res.content)


@app.route("/kairos/tagvalues")
def list_tagvalues():
    """
    List all available tag values
    """
    res = requests.get(generate_base_url() + "/tagvalues", auth=(conn.user, conn.passw))
    return res.content


@app.route("/kairos/core")
def core_level():
    """Load data on per-core level in dygraphs-friendly format
    Designed for association with job info where you pick the nodes (at least!)

    Params:
        from    <required>  timestamp
        to                  timestamp
        metric  <required>  metric by which to query
        node    <list>      list of nodes to query
        core    <list>      list of cores to query
        raw                 return KairosDB data format (no post-processing)
        aggregate   <def:5> size of time window (s) in which to aggregate data (and alignment of timestamps)
    """
    args = request.args.to_dict()

    args["node"] = request.args.getlist("node")
    metrics = request.args.getlist("metric")

    res = list()

    if len(args["node"]) == 0:
        raise JobsError("Node list must be specified")

    args["core"] = request.args.getlist("core")

    for item in metrics:
        res.append(load_data(args['job_id'], item))

    return json.dumps(join_data(res))


@app.route("/kairos/cpu")
def cpu_level():
    """
    Load data on per-cpu level in dygraphs-friendly format
    Designed for association with job info where you pick the nodes (at least!)

    Params:
        from    <required>  timestamp
        to                  timestamp
        metric  <required>  metric by which to query
        node    <list>      list of nodes to query
        cpu     <list>      list of cpus to query
        raw                 return KairosDB data format (no post-processing)
        aggregate   <def:5> size of time window (s) in which to aggregate data (and alignment of timestamps)
    """
    args = request.args.to_dict()

    args["node"] = request.args.getlist("node")
    metrics = request.args.getlist("metric")

    res = list()

    if len(args["node"]) == 0:
        raise JobsError("Node list must be specified")

    args["cpu"] = request.args.getlist("cpu")

    for item in metrics:
        res.append(load_data(args['job_id'], item))

    return json.dumps(join_data(res))


@app.route("/kairos/node")
def load_base():
    """
    Load data on per-node level in dygraphs-friendly format

    Params:
        from    <required>  timestamp
        to                  timestamp
        metric  <required>  metric by which to query
        raw                 return KairosDB data format (no post-processing)
        aggregate   <def:5> size of time window (s) in which to aggregate data (and alignment of timestamps)
    """
    args = request.args.to_dict()

    args["node"] = request.args.getlist("node")
    metrics = request.args.getlist("metric")

    res = list()

    for item in metrics:
        res.append(load_data(args['job_id'], item))

    return json.dumps(join_data(res))


@app.route("/kairos/cluster")
def cluster_level():
    """
    Load data on per-cluster level in dygraphs-friendly format

    Params:
        from    <required>  timestamp
        to                  timestamp
        metric  <required>  metric by which to query
        raw                 return KairosDB data format (no post-processing)
        aggregate   <def:5> size of time window (s) in which to aggregate data (and alignment of timestamps)
    """
    args = request.args.to_dict()
    args["node"] = request.args.getlist("node")
    metrics = request.args.getlist("metric")
    res = list()

    for item in metrics:
        res.append(load_data(args['job_id'], item, grouper='cluster'))

    return json.dumps(join_data(res))


def query(args, aggregate_window, group_tags, modifying_func="aggregate", tags=None):
    check_times(args)

    agg = Aggregate(aggregate_window)
    agg.set_group_tags(group_tags)

    if len(args["metric"]) == 0:
        raise JobsError("Missing 'metric' in GET parameters")

    if "aggregate" in args:
        agg.set_window(int(args["aggregate"]))

    if modifying_func == "aggregate":
        mod_func = agg.aggregate
    elif modifying_func == "gaps":
        mod_func = agg.gaps
    else:
        mod_func = modifying_func

    if not tags:
        tags_parsed = {
                    "org": config["kairosdb"].get("org", "cineca"),
                    "cluster": config["kairosdb"].get("cluster", "galileo")
                }
    else:
        tags_parsed = merge_dicts({
                "org": config["kairosdb"].get("org", "cineca"),
                "cluster": config["kairosdb"].get("cluster", "galileo")
            }, tags)

    res = reader.read(conn,
            args["metric"],
            start_absolute=args["from"],
            end_absolute=args["to"],
            tags=tags_parsed,
            query_modifying_function=mod_func
            )

    if "raw" in args:
        return res

    if res["queries"][0]["sample_size"] == 0:
        raise JobsError("No data found", status_code=404)

    labels = list()
    data = dict()

    extract_data(res, data, labels, group_tags)

    return({
        "points": data,
        "labels": labels,
        "metric": res["queries"][0]["results"][0]["name"]
    })

