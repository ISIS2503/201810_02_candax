# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
import datetime
import tornado.web
import tornado.escape
import candax.rest as rest
from candax.auth import jwtauth
import uuid

LOGGER = logging.getLogger(__name__)
bucket = 'passwords_history'
bucket_o ='owners'


class MainHandler(rest.BaseHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def post(self, *args):
        k = str(uuid.uuid1().int)
        self.json_args['key'] = k
        _history = yield self.application.db.insert(bucket, self.json_args)
        owner_s = yield self.application.db.get(bucket_o, self.json_args['owner'])
        owner_s['passwords'].update({self.json_args['pos']:self.json_args['pass']})
        objs = yield self.application.db.update(bucket_o, owner_s)
        message = 'CHANGE_PASSWORD;' + self.json_args['pos'] + ';' + self.json_args['pass']
        print(message)
        self.application.clientMQTT.publish_message(message)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)
