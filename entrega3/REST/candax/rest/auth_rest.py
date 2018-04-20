# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
import datetime
import jwt
import tornado.web
import tornado.escape
import candax.rest as rest
import uuid

LOGGER = logging.getLogger(__name__)
bucket = 'administrators'

SECRET = 'my_secret_key'


class MainHandler(rest.BaseHandler):
    def initialize(self, db=None):
        self.db = db

    """
        Handle to auth method.
        This method aim to provide a new authorization token
        There is a fake payload (for tutorial purpose)
    """
    def prepare(self):
        """
            Encode a new token with JSON Web Token (PyJWT)
        """
        self.encoded = jwt.encode({
            'some': 'payload',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600)},
            SECRET,
            algorithm='HS256'
        )

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        """
            return the generated token
        """
        print('PINNGGG')
        response = {'token': self.encoded.decode('ascii')}
        self.write(response)
