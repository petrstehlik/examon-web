from liberouterapi import socketio, config
from flask_socketio import send, emit, join_room, leave_room
from ..jobs import jobman
from ..utils import *
import json

import logging

log = logging.getLogger(__name__)

subscribed_jobs = dict()

@socketio.on('subscribe', namespace='/jobs')
def subscribe_job(json_data):
    global subscribed_jobs

    log.info("Received subscribe message: %s" % json)

    jobid = json_data['jobid']

    if jobid in jobman.db:
        if jobid in subscribed_jobs:
            subscribed_jobs[jobid] += 1
        else:
            subscribed_jobs[jobid] = 1

        join_room(jobid)

        try:
            emit('data',
                    json.dumps(transform_live_job(jobid, jobman), default=time_serializer),
                    room = jobid)
        except KeyError as e:
            log.error("Cannot find job: %s" % str(e))
    else:
        emit('error', "Can't find job in database")

@socketio.on('unsubscribe', namespace='/jobs')
def unsubscribe_job(json_data):
    global subscribed_jobs

    log.info("Received unsubscribe message: %s" % json_data)

    if 'jobid' in json_data:
        jobid = json_data['jobid']
        try:
            log.info("Unsubscribing from %s" % jobid)

            if jobid in subscribed_jobs:
                if subscribed_jobs[jobid] > 0:
                    subscribed_jobs[jobid] -= 1
                else:
                    emit('error', "No subscriber in the room")

                if subscribed_jobs[jobid] == 0:
                    del subscribed_jobs[jobid]
            else:
                emit('error', "Room doesn't exist")

            leave_room(jobid)
        except KeyError as e:
            emit('error', "Cannot find given job '%s'" % jobid)

    else:
        emit('error', "Missing 'jobid' in request")

def emit_data(jobid):
    global subscribed_jobs

    if jobid in subscribed_jobs and subscribed_jobs[jobid] > 0:
        log.info("Emiting new data: %s" % jobman.db[jobid])

    socketio.server.emit('data',
            json.dumps(transform_live_job(jobid, jobman), default=time_serializer),
            namespace = '/jobs',
            room = jobid)

