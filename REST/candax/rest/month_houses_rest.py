# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
import datetime
import tornado.web
import tornado.escape
import candax.rest as rest

LOGGER = logging.getLogger(__name__)
bucket = 'alarms'

class MainHandler(rest.BaseHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def get(self, _id=None):
        if _id is None:
            print('Error, debe agregar un RU para buscar')
        else:
            _id = _id.replace("_", " ")
            objs = yield self.application.db.get_month(bucket, _id, 'house')
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)
