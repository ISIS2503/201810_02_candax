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
bucket_a = 'administrators'

@jwtauth
class MainHandler(rest.BaseHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def get(self, _id=None):
        if _id is None:
            objs= {"Error": "debe agregar un RU para buscar"}
            self.set_status(400)
        else:
            data_admin = yield self.application.db.get(bucket_a, _id)
            if data_admin is None:
                objs= {"Error": "id no existe"}
                self.set_status(400)
            else:
                s = data_admin['res_unit'][0]
                objs = yield self.application.db.get_all_user(bucket, s, 'Admin')
                self.set_status(201)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)
