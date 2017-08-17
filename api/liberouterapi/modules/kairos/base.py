from liberouterapi import config, app
from .error import JobsError
from .utils import check_times, generate_health_url, generate_base_url, extract_data, merge_dicts, join_data
from .Aggregate import Aggregate

from flask import request
from pyKairosDB import connect, metadata, reader
import json
import requests

conn = connect(server = config["kairosdb"].get("server"),
        port = config["kairosdb"].get("port"),
        user = config["kairosdb"].get("user"),
        passw = config["kairosdb"].get("password"))

@app.route("/kairos/health")
def health():
    res = requests.get(generate_health_url() + "/check", auth=(conn.user, conn.passw))
    return('', res.status_code)

@app.route("/kairos/status")
def status():
	res = requests.get(generate_health_url() + "/status", auth=(conn.user, conn.passw))
	return(str(res.content))

@app.route("/kairos/metrics")
def list_metrics():
    """
    List all available metrics
    """
    res = requests.get(generate_base_url() + "/metricnames", auth=(conn.user, conn.passw))
    return(str(res.content))

@app.route("/kairos/tags")
def list_tags():
    """
    List all available metrics
    """
    res = requests.get(generate_base_url() + "/tagnames", auth=(conn.user, conn.passw))
    return(str(res.content))

@app.route("/kairos/core")
def core_level():
    """
    Load data on per-core level in dygraphs-friendly format
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
        args["metric"] = [item]
        res.append(query(args, 2, ['node', 'core'], tags = {
                "node" : args["node"]
            }))

    return(json.dumps(join_data(res)))

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
        args["metric"] = [item]
        res.append(query(args, 25, ['node', 'cpu'], tags = {
                "node" : args["node"]
            }))

    return(json.dumps(join_data(res)))

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

    res_list = list()

    if len(args["node"]) > 0:
        for item in metrics:
            args["metric"] = [item]
            res_list.append(query(args, 5, ['node'], tags = {
                "node" : args["node"]
            }))

        return(json.dumps(join_data(res_list)))
    else:
        args["metric"] = [args["metric"]]
        res_list.append(query(args, 5, ['node']))

    return(json.dumps(join_data(res_list)))


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
    res_list = list()

    if len(args["node"]) > 0:
        for item in metrics:
            args["metric"] = [item]
            res_list.append(query(args, 5, ['cluster'], tags = {
                "node" : args["node"]
            }))

        return(json.dumps(join_data(res_list)))
    else:
        args["metric"] = [args["metric"]]
        res_list.append(query(args, 5, ['cluster']))

    return(json.dumps(join_data(res_list)))

def query(args, aggregate_window, group_tags, modifying_func = "aggregate", tags = None):
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

    if tags == None:
        tags_parsed = {
                    "org" : ["cineca"],
                    "cluster" : ["galileo"]
                }
    else:
        tags_parsed = merge_dicts({
                "org" : ["cineca"],
                "cluster" : ["galileo"]
            }, tags)

    res = reader.read(conn,
            args["metric"],
            start_absolute = args["from"] / 1000,
            end_absolute = args["to"] / 1000,
            tags = tags_parsed,
            query_modifying_function = mod_func
            )

    if "raw" in args:
        return(res)

    if res["queries"][0]["sample_size"] == 0:
        raise JobsError("No data found", status_code=404)

    labels = list()
    data = dict()

    extract_data(res, data, labels, group_tags)

    return({
        "points" : data,
        "labels" : labels,
        "metric" : res["queries"][0]["results"][0]["name"]
    })

