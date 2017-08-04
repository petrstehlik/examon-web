from liberouterapi import app
from liberouterapi.error import ApiException
from ..module import Module

from flask import Blueprint, request

from Holder import Holder

import json

class MqttError(ApiException):
    status_code = 500

mqtt = Blueprint('mqtt', __name__, url_prefix = '/mqtt')

holder = Holder("130.186.13.80", mqtt_topics = ["org/cineca/cluster/galileo/node/+/plugin/#"])

def split_list(values, delim = ","):
    """
    Remove all whitespaces and split by delimiter
    """
    return values.replace(" ", "").split(delim)

def merge_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

@mqtt.route('/metric/<string:metric>')
def get_metric(metric):
    print(metric)

    return(json.dumps(holder.db[metric]))

@mqtt.route('/node')
def get_nodes():
    return(json.dumps(holder.nodes))


