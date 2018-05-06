# -*- coding: utf-8 -*-
# !/usr/bin/env python3

"""LangVisNet backend Python server."""

# Standard lib imports
import os
import sys
import logging
import argparse
import jwt
import datetime
import os.path as osp
from candax.auth import jwtauth

# Tornado imports
import tornado.web
import tornado.ioloop

# Local imports
from candax.db import RiakDB
from candax.mqtt_client import clientMQTT
from candax.routes import ROUTES

# Other library imports
import coloredlogs

parser = argparse.ArgumentParser(
    description='Un servidor muy bonito')

# pbc://172.24.41.149:8087
# pbc://localhost:8087

parser.add_argument('--riak-url', type=str, default='pbc://172.24.41.149:8087',
                    help='Riak url endpoint used to locate DB')
parser.add_argument('--port', type=int, default=8000,
                    help='TCP port used to deploy the server')
parser.add_argument('--mqtt-url', type=str, default='http://172.24.41.153:8083',
                    help='MQTT url endpoint used to locate server')
parser.add_argument('--mqtt-name', type=str, default='server_client_1',
                    help='MQTT url endpoint used to locate server')

# AMQP_URL = ('amqp://langvis_server:eccv2018-textseg@margffoy-tuay.com:5672/'
#             'queryobjseg')

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
coloredlogs.install(level='info')

args = parser.parse_args()

clr = 'clear'
if os.name == 'nt':
    clr = 'cls'


def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    settings = {"static_path": os.path.join(
        os.path.dirname(__file__), "static"), "xsrf_cookies": False, }
    application = tornado.web.Application(
        ROUTES, debug=True, serve_traceback=True, autoreload=True,
        **settings)
    LOGGER.info("Server is now at: 127.0.0.1:8000")
    ioloop = tornado.ioloop.IOLoop.instance()

    application.db = RiakDB(args.riak_url)
    LOGGER.info('Data base Riak connected')
    # application.clientMQTT = clientMQTT(args.mqtt_name, args.mqtt_url)
    # LOGGER.info('Client MQTT connected')
    application.listen(args.port)
    try:
        ioloop.start()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing server...\n")
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    os.system(clr)
    main()
