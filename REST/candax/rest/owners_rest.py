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
bucket = 'owners'


@jwtauth
class MainHandler(rest.BaseHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def get(self, _, _id=None):
        if _id is None:
            objs = yield self.application.db.get_all(bucket)
        else:
            objs = yield self.application.db.get(bucket, _id)
        # self.set_status(403)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)

    @tornado.gen.coroutine
    def post(self, *args):
        # alarm = {'house': ; 'res_unit': ; 'hub': ; 'lock': ; 'date':}
        passwords = {'1': '', '2': '', '3': '', '4': '', '5': '', '6': '',
                     '7': '', '8': '', '9': '', '10': '', '11': '', '12': '',
                     '13': '', '14': '', '15': '', '16': '', '17': '',
                     '18': '', '19': '', '20': ''}
        self.json_args['passwords'] = passwords
        _id = yield self.application.db.insert(bucket, self.json_args)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(_id)

    @tornado.gen.coroutine
    def put(self, *args):
        # print("MSG: {0}".format(self.application.db is None))
        #bucket = 'test'
        objs = yield self.application.db.update(bucket, self.json_args)
        # self.set_status(403)
        print(objs)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)

    @tornado.gen.coroutine
    def delete(self, _, _id=None):
        #bucket = 'test'
        print(_id)
        if _id is None:
            #objs = yield self.application.db.get_all(bucket)
            print('no hay naditaaaaa')
        else:
            objs = yield self.application.db.delete(bucket, _id)
        # self.set_status(403)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)
