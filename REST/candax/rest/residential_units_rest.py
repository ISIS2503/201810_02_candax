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
bucket = 'residential_units'


# @jwtauth
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
            if objs is None:
                self.set_status(400)
                objs = {"Error": "Object does not exist"}
            else:
                self.set_status(201)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)

    @tornado.gen.coroutine
    def post(self, *args):
        if self.json_args is not None:
            objs = yield self.application.db.get(bucket, self.json_args['key'])
            if objs is not None:
                self.set_status(400)
                response = {"Error": "The object already exist"}
            else:
                tree = yield self.application.db.get("tree", self.json_args["security"])
                toAppend = {"name":self.json_args["name"] , "children": []}
                if tree is None:
                    self.set_status(400)
                    print(tree)
                    response = {"Error": "There is no private security with the id provided"}

                else:
                    print("entra")
                    response = yield self.application.db.insert(bucket, self.json_args)
                    tree["data"]["children"].append(toAppend)
                    self.application.db.update("tree", tree)
                    self.set_status(201)
        else:
            self.set_status(400)
            response = "Error: Content-Type must be application/json"
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(response)

    @tornado.gen.coroutine
    def put(self, *args):
        if self.json_args is not None:
            objs = yield self.application.db.get(bucket, self.json_args['key'])
            if objs is None:
                self.set_status(400)
                objs = {"Error": "The object does not exist"}
            else:
                objs = yield self.application.db.update(bucket, self.json_args)
                self.set_status(201)
        else:
            self.set_status(400)
            objs = {"Error": "No content type"}
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)

    @tornado.gen.coroutine
    def delete(self, _, _id=None):
        if _id is not None:
            objs = yield self.application.db.delete(bucket, _id)
            if objs is None:
                self.set_status(400)
                objs = {"Error": "The object does not exist"}
            else:
                self.set_status(201)
        else:
            self.set_status(400)
            objs = {"Error": "No id"}
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)
