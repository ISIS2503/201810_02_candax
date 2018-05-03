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
bucket_o = 'owners'


class MainHandler(rest.BaseHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def get(self, _id=None):
        if _id is None:
            print('jkdasjdklsadja')
        else:
            data_owner = yield self.application.db.get(bucket_o, _id)
            s = data_owner['res_unit'] + ';' + data_owner['house']
            objs = yield self.application.db.get_all_user(bucket, s, 'Owner')
        # self.set_status(403)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)
