from liberouterapi import app, socketio
from liberouterapi.error import ApiException
from ..module import Module

from flask import Blueprint, request
from flask_socketio import send, emit, join_room, leave_room

from Holder import Holder

import json

class MqttError(ApiException):
    status_code = 500

mqtt = Blueprint('mqtt', __name__, url_prefix = '/mqtt')


subscribed_metrics = list()

def emit_data(node, metric, data):
    global subscribed_metrics

    if metric in subscribed_metrics:
        socketio.server.emit('data', {
            'metric' : metric,
            'node' : node,
            'data' : data,
            'range' : holder.minmax(metric)
            },
            namespace='/render',
            room = metric)

holder = Holder("130.186.13.80", mqtt_topics = ["org/cineca/cluster/galileo/node/+/plugin/#"])
holder.on_store = emit_data

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

@socketio.on('subscribe-metric', namespace='/render')
def handle_my_custom_event(json):
    global subscribed_metrics
    if 'metric' in json:
        try:
            subscribed_metrics.append(json['metric'])
            join_room(json['metric'])
            emit('initial-data', holder.db[json['metric']], room = json['metric'])
        except KeyError as e:
            emit('error', "Cannot find given metric '%s'" % json['metric'])

    else:
        emit('error', "Missing metric in request")

@socketio.on('unsubscribe-metric', namespace='/render')
def handle_my_custom_event(json):
    global subscribed_metrics
    if 'metric' in json:
        try:
            print("UNSUBSCRIBING")
            #subscribed_metrics.append(json['metric'])
            leave_room(json['metric'])
        except KeyError as e:
            emit('error', "Cannot find given metric '%s'", json['metric'])

    else:
        emit('error', "Missing metric in request")
