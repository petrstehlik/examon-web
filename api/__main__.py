#!/usr/bin/env python3

from muapi import app, config

if __name__ == '__main__':
    app.run(port = app.config["PORT"],
            host = app.config["HOST"])
