from liberouterapi import config, app

from pyKairosDB import connect, metadata, reader
import json
import requests

conn = connect(server = config["kairosdb"].get("server"),
        port = config["kairosdb"].get("port"),
        user = config["kairosdb"].get("user"),
        passw = config["kairosdb"].get("password"))

base_query = {
            "start_absolute" : 1500554800.000,
            "end_absolute" : 1500555005,
            "metrics" : [
                    {
                        "tags" : {
                            "org" : ["cineca"],
                            "cluster" : ["galileo"],
                            "node" : ["node062"],
                            #"core" : ["0", "1"]
                        }
                    }
                ]
        }

fra = {
  "metrics": [
    {
      "tags": {
          "org": [
              "cineca"
          ],
          "cluster": [
            "galileo"
          ],
          "node": [
            "node061"
          ]
      },
      "name": "temp",
      "group_by": [
        {
            "name": "tag",
           "tags": [
              "core"
            ]
        }
      ]
    }
  ],
  "cache_time": 0,
  "start_relative": {
    "value": "1",
    "unit": "minutes"
  }
}

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

def group(query):
    query["metrics"][0]["group_by"] = [
        {
            "name": "tag",
            "tags": [
                "core"
            ]
        }]
    print(query)
    return query

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
