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
bucket = 'houses'


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
                resUnit = yield self.application.db.get("residential_units", self.json_args["res_unit"])
                if(resUnit is None):
                    self.set_status(400)
                    response = {
                        "Error": "There is no residential unit with the provided id."}
                else:
                    # se agrega al bucket
                    response = yield self.application.db.insert(bucket, self.json_args)
                    # se agrega al arbol
                    tree = yield self.application.db.get("tree", resUnit["security"])
                    for resUnitTree in tree["data"]["children"]:
                        if resUnitTree["attributes"]["name"] == resUnit["name"]:
                            resUnitTree["children"].append(
                                                        {
                                                        "name": self.json_args["key"],
                                                        "nodeSvgShape": {
                                                          "shape": "circle",
                                                          "shapeProps": {
                                                            "r": 10,
                                                            "fill": "#04B4AE"
                                                          }
                                                        }}
                                                        )
                            break
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
                # se borra del arbol
                resUnit = yield self.application.db.get("residential_units", objs["res_unit"])
                tree = yield self.application.db.get("tree", resUnit["security"])

                for resUnitTree in tree["data"]["children"]:
                        if resUnitTree["name"] == resUnit["name"]:
                            cont = 0
                            for casita in resUnitTree["children"]:
                                if casita["name"] == _id:
                                    break
                                cont += 1
                            resUnitTree["children"].pop(cont)
                            break


                self.application.db.update("tree", tree)
                self.set_status(201)
        else:
            self.set_status(400)
            objs = {"Error": "No id"}
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)
