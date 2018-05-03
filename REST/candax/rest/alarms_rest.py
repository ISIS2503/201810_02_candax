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

LOGGER = logging.getLogger(__name__)
bucket = 'alarms'


# alarm = {'house': ; 'res_unit': ; 'hub': ; 'lock': ; 'date':}
@jwtauth
class MainHandler(rest.BaseHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def get(self, _, _id=None):
        if _id is None:
            objs = yield self.application.db.get_all(bucket)
            self.set_status(201)
        else:
            objs = yield self.application.db.get(bucket, _id)
            self.set_status(201)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)

    @tornado.gen.coroutine
    def post(self, *args):
        if self.json_args is not None:
            response = yield self.application.db.insert(bucket, self.json_args)
            self.set_status(201)
        else:
            self.set_status(400)
            response = "Error: Content-Type must be application/json"
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(response)

    @tornado.gen.coroutine
    def put(self, *args):
        if self.json_args is not None:
            objs = yield self.application.db.update(bucket, self.json_args)
            self.set_status(201)
        else:
            self.set_status(400)
        # print(objs)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)

    @tornado.gen.coroutine
    def delete(self, _, _id=None):
        print(_id)
        if _id is not None:
            objs = yield self.application.db.delete(bucket, _id)
            self.set_status(201)
        else:
            self.set_status(400)
            objs = "Error: id undefined"
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)
