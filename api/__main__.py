#!/usr/bin/env python3
import logging

logging.basicConfig(level=logging.DEBUG)

from muapi import socketio, config, app, auth
from modules.remote_pam.ssh import RemotePAM

if __name__ == '__main__':
    app.config.from_object(config)
    auth.pam = RemotePAM()
    socketio.run(app, debug=config['api'].get('debug', False), port=config['api'].getint('port', 5555))
            #port = app.config["PORT"],
            #host = app.config["HOST"])

