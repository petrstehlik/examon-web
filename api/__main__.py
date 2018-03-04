#!/usr/bin/env python3
import logging

logging.basicConfig(level=logging.DEBUG)

from muapi import socketio, config, app

if __name__ == '__main__':
    app.config.from_object(config)
    socketio.run(app, debug=True, port=5555)
            #port = app.config["PORT"],
            #host = app.config["HOST"])
