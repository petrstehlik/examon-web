from liberouterapi import config, app
from .error import JobsError
from .utils import check_times, generate_health_url, generate_base_url, extract_data
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
    print(res.content)
    return(str(res.content))

@app.route("/kairos/tags")
def list_tags():
    """
    List all available metrics
    """
    res = requests.get(generate_base_url() + "/tagnames", auth=(conn.user, conn.passw))
    print(res.content)
    return(str(res.content))

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

    check_times(args)

    agg = Aggregate(5)
    agg.set_tags(['node'])

    if "metric" not in args:
        raise JobsError("Missing 'metric' in GET parameters")

    if "aggregate" in args:
        agg.set_window(int(args["aggregate"]))

    res = reader.read(conn,
            [args["metric"]],
            start_absolute = args["from"] / 1000,
            end_absolute = args["to"] / 1000,
            tags = {
                "org" : ["cineca"],
                "cluster" : ["galileo"]
            },
            query_modifying_function = agg.aggregate
            )

    if "raw" in args:
        return(json.dumps(res))

    labels = list()
    data = dict()

    extract_data(res, data, labels, "node")

    return(json.dumps({
        "points" : data,
        "labels" : labels,
        "metric" : res["queries"][0]["results"][0]["name"]
    }))

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

    check_times(args)

    agg = Aggregate(5)
    agg.set_tags(['cluster'])

    if "metric" not in args:
        raise JobsError("Missing 'metric' in GET parameters")

    metric = args["metric"]

    if "aggregate" in args:
        agg.set_window(int(args["aggregate"]))

    res = reader.read(conn,
            [args["metric"]],
            start_absolute = args["from"] / 1000,
            end_absolute = args["to"] / 1000,
            tags = {
                "org" : ["cineca"],
                "cluster" : ["galileo"]
            },
            query_modifying_function = agg.aggregate
            )

    if "raw" in args:
        return(json.dumps(res))

    labels = list()
    data = dict()

    extract_data(res, data, labels, "cluster")

    return(json.dumps({
        "points" : data,
        "labels" : labels,
        "metric" : res["queries"][0]["results"][0]["name"]
    }))

