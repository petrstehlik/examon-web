from liberouterapi import config, app

from pyKairosDB import connect, metadata, reader
import json
import requests

conn = connect(server="130.186.13.80", port=8010,
        user=config["kairosdb"].get("user"),
        passw=config["kairosdb"].get("password"))

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
