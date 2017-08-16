from liberouterapi import app, socketio, config
from liberouterapi.error import ApiException
from ..module import Module
from ..utils import split_list, merge_dicts
from Holder import Holder

from flask import Blueprint, request
from flask_socketio import send, emit, join_room, leave_room
import json
import logging

class MqttError(ApiException):
    status_code = 500

mqtt = Blueprint('mqtt', __name__, url_prefix = '/mqtt')

log = logging.getLogger(__name__)

subscribed_metrics = dict()

def emit_data(node, metric, data):
    global subscribed_metrics

    if metric in subscribed_metrics and subscribed_metrics[metric] > 0:
        log.debug("Unsubscribed metric: %s", json.dumps(subscribed_metrics[metric]))
        socketio.server.emit('data', {
            'metric' : metric,
            'node' : node,
            'data' : data,
            'range' : holder.minmax(metric)
            },
            namespace='/render',
            room = metric)

# Initialize Holder with config topics
holder = Holder(config['mqtt']['server'],
        mqtt_topics = json.loads(config['mqtt']['topics']))
holder.on_store = emit_data

@mqtt.route('/metric/<string:metric>')
def get_metric(metric):
    """
    Return given metric data from a holder
    """
    try:
        return(json.dumps(holder.db[metric]))
    except KeyError as e:
        raise MqttError("Metric %s not found in holder's DB" % metric, status_code=404)

@mqtt.route('/node')
def get_nodes():
    return(json.dumps(holder.nodes))

@socketio.on('subscribe-metric', namespace='/render')
def subscribe_metric(json):
    global subscribed_metrics
    if 'metric' in json:
        metric = json['metric']
        try:
            if metric in subscribed_metrics:
                subscribed_metrics[metric] += 1
            else:
                subscribed_metrics[metric] = 1

            join_room(metric)
            emit('initial-data', holder.db[metric], room = metric)
        except KeyError as e:
            emit('error', "Cannot find given metric '%s'" % metric)

    else:
        emit('error', "Missing metric in request")

@socketio.on('unsubscribe-metric', namespace='/render')
def unsubscribe_metric(json):
    global subscribed_metrics
    if 'metric' in json:
        metric = json['metric']
        try:
            log.info("Unsubscribing from %s" % metric)

            if metric in subscribed_metrics:
                if subscribed_metrics[metric] > 0:
                    subscribed_metrics[metric] -= 1
                else:
                    emit('error', "No subscriber in the room")

                if subscribed_metrics[metric] == 0:
                    del subscribed_metrics[metric]
            else:
                emit('error', "Room doesn't exist")

            leave_room(metric)
        except KeyError as e:
            emit('error', "Cannot find given metric '%s'" % metric)

    else:
        emit('error', "Missing metric in request")
