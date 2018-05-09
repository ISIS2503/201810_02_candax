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
from requests import post

LOGGER = logging.getLogger(__name__)


# @jwtauth
class MainHandler(rest.BaseHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def post(self, *args):
        print("entra")
        temp =  post('http://localhost:8089/silence', json={"whatev":"asda"})
        print(temp)
        return temp
