from liberouterapi import config, app

from flask import request

from pyKairosDB import connect, metadata, reader
import json
import requests

conn = connect(server = config["kairosdb"].get("server"),
        port = config["kairosdb"].get("port"),
        user = config["kairosdb"].get("user"),
        passw = config["kairosdb"].get("password"))

base_query = {
    "start_absolute" :  1500554860,
    "end_absolute" :    1500554900,
    "metrics" : [
            {
                "tags" : {
                    "org" : ["cineca"],
                    "cluster" : ["galileo"]
                }
            }
        ]
    }

def generate_base_url():
    return("{0}://{1}:{2}/api/v1".format(conn.schema, conn.server, conn.port))

def generate_health_url():
    return("{0}://{1}:{2}/api/v1/health".format(conn.schema, conn.server, conn.port))

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

def group(query):
    return group_tags(query, ["core", "node"])

def group_tags(query, tags):
    query["metrics"][0]["group_by"] = [
        {
            "name": "tag",
            "tags": tags
        }]
    return query

def group_nodes(query):
    return group_tags(query, ["node"])

def agg_and_group(query):
    #query = group(query)
    query["metrics"][0]["aggregators"] = [
            {
                "name" : "avg",
                #"align_sampling" : True,
                "sampling" : {
                        "value" :(base_query["end_absolute"] - base_query["start_absolute"]),
                        "unit" : "minutes"
                    }
            }]
    return query

def aggregate_5_secs(query):
    #query = group(query)
    q2 = group_tags(query, ["node"])
    q2["metrics"][0]["aggregators"] = [
            {
                "name" : "avg",
                "align_sampling" : True,
                "align_start_time" : True,
                "sampling" : {
                        "value" : 10,
                        "unit" : "seconds"
                    }
            }]
    return q2


@app.route("/kairos/basic")
def basic():
    res= reader.read(conn,
            ["temp"],
            start_absolute = base_query["start_absolute"],
            #start_relative = (5, "minutes"),
            end_absolute = base_query["end_absolute"],
            tags = base_query["metrics"][0]["tags"],
            query_modifying_function = group
            #tags = {"node" : ["node061"]}
            #only_read_tags = True
            )

    return(json.dumps(res))

@app.route("/kairos/sum")
def sum_base():
    res= reader.read(conn,
            ["temp"],
            start_absolute = base_query["start_absolute"],
            end_absolute = base_query["end_absolute"],
            tags = base_query["metrics"][0]["tags"],
            query_modifying_function = agg_and_group
            #tags = {"node" : ["node061"]}
            #only_read_tags = True
            )

    return(json.dumps(res))


@app.route("/kairos/load")
def load_base():
    args = request.args.to_dict()

    if "from" in args:
        # Convert to int so we can compare it
        args["from"] = int(args["from"])
    else:
        raise JobsError("Missing 'from' in GET parameters")

    if "to" not in args:
        # Generate timestamp
        args["to"] = int(time.time()) * 1000
    else:
        args["to"] = int(args["to"])

    if args["to"] < args["from"]:
        raise JobsError("'from' time cannot precede 'to' time")


    res= reader.read(conn,
            ["load_core"],
            start_absolute = args["from"] / 1000,
            end_absolute = args["to"] / 1000,
            tags = base_query["metrics"][0]["tags"],
            query_modifying_function = aggregate_5_secs
            )

    if "raw" in args:
        return(json.dumps(res))

    labels = list()
    data = dict()

    for result in res["queries"][0]["results"]:
        labels.append(result["group_by"][0]["group"]["node"])
        for item in result["values"]:
            round_time = int(round(item[0], -1))

            if str(round_time) not in data:
                data[str(round_time)] = [item[1]]
            else:
                data[str(round_time)].append(item[1])

    return(json.dumps({
        "points" : data,
        "labels" : labels,
        "metric" : res["queries"][0]["results"][0]["name"]
    }))

