from muapi import app, socketio, config
from muapi.error import ApiException
from muapi.Module import Module
from utils import split_list, merge_dicts
from Holder import Holder

from flask import Blueprint, request
from flask_socketio import send, emit, join_room, leave_room
import json
import logging
from time import sleep


class MqttError(ApiException):
    status_code = 500


mqtt = Module('mqtt', __name__, url_prefix = '/mqtt', no_version=True)

log = logging.getLogger(__name__)

subscribed_metrics = dict()

metrics = {
    'M4WR_MEM': 'ame_pub/chnl/data/occ/2/cmp/MEM/id/+/unt/GBs/M4WR_MEM',
    'UTIL_P0': 'ame_pub/chnl/data/occ/2/cmp/CORE/id/+/unt/Per/UTIL_P0',
    'TEMP_P0': 'ame_pub/chnl/data/occ/1/cmp/CORE/id/9/unt/C/TEMP_P0',
    'GPU_Power': 'ipmi_pub/chnl/data/GPU_Power',
    'Fan_Power': 'ipmi_pub/chnl/data/Fan_Power',
    'Proc0_Power': 'ipmi_pub/chnl/data/Proc0_Power',
    'Proc1_Power': 'ipmi_pub/chnl/data/Proc1_Power',
    'Ambient_Temp': 'ipmi_pub/chnl/data/Ambient_Temp',
}


def emit_data(node, metric, data):
    global subscribed_metrics

    if metric in subscribed_metrics and subscribed_metrics[metric] > 0:
        log.debug("Metric: %s (subscribers: %s)", metric, subscribed_metrics[metric])
        socketio.server.emit('data', {
                'metric': metric,
                'node': node,
                'data': data,
                'range': holder.minmax(metric)
            },
            namespace='/render',
            room=metric)


# Initialize Holder with config topics
holder = Holder(config['mqtt']['server'])
holder.on_store = emit_data


@mqtt.route('/metric/<string:metric>')
def get_metric(metric):
    """
    Return given metric data from a holder
    """
    try:
        return json.dumps(holder.db[metric])
    except KeyError as e:
        raise MqttError("Metric %s not found in holder's DB" % metric, status_code=404)


@mqtt.route('/nodes')
def get_nodes():
    return json.dumps(holder.nodes)


@socketio.on('subscribe-metric', namespace='/render')
def subscribe_metric(data):
    global subscribed_metrics
    global metrics
    if 'metric' in data:
        metric = data['metric']
        try:
            if metric in subscribed_metrics:
                subscribed_metrics[metric] += 1
            else:
                subscribed_metrics[metric] = 1
                holder.subscribe(metrics[metric])

            join_room(metric)
            sleep(5)
            emit('initial-data', holder.db[metric], room=metric)
        except KeyError as e:
            emit('error', "Cannot find given metric '%s'" % metric)

    else:
        emit('error', "Missing metric in request")


@socketio.on('unsubscribe-metric', namespace='/render')
def unsubscribe_metric(json):
    global subscribed_metrics
    global metrics
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
                    holder.unsubscribe(metrics[metric])
            else:
                emit('error', "Room doesn't exist")

            leave_room(metric)
        except KeyError as e:
            emit('error', "Cannot find given metric '%s'" % metric)

    else:
        emit('error', "Missing metric in request")
