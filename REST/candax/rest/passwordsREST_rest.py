
import json
import logging
import tornado.web
import tornado.escape
import tornado.httpclient as httpclient
from requests import post as posty
import candax.rest as rest
from candax.auth import jwtauth
import uuid

LOGGER = logging.getLogger(__name__)
bucket = 'passwords'

@jwtauth
class MainHandler(rest.BaseHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        objs = yield self.application.db.get_all(bucket)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        client = httpclient.AsyncHTTPClient()
        h = {'Content-Type': 'application/json; charset=UTF-8'}
        request = httpclient.HTTPRequest(url='http://localhost:5000/pwds',
                                         method='POST',
                                         body=json.dumps(self.json_args),
                                         headers=h)
        print(self.json_args)
        response = client.fetch(request)
        k = str(uuid.uuid1().int)
        self.json_args['key'] = k
        yield self.application.db.insert(bucket, self.json_args)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(self.json_args)

    @tornado.gen.coroutine
    def put(self, *args, **kwargs):
        client = httpclient.AsyncHTTPClient()
        h = {'Content-Type': 'application/json; charset=UTF-8'}
        request = httpclient.HTTPRequest(url='http://localhost:5000/pwds',method='POST',body=json.dumps(self.json_args),headers=h)
        print(self.json_args)
        response = client.fetch(request)
        k = str(uuid.uuid1().int)
        self.json_args['key'] = k
        yield self.application.db.insert(bucket, self.json_args)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(self.json_args)

    @tornado.gen.coroutine
    def delete(self, *args, **kwargs):
        client = httpclient.AsyncHTTPClient()
        self.json_args['pass'] = '0000'
        h = {'Content-Type': 'application/json; charset=UTF-8'}
        request = httpclient.HTTPRequest(url='http://localhost:5000/pwds',method='POST',body=json.dumps(self.json_args),headers=h)
        print(self.json_args)
        response = client.fetch(request)
        k = str(uuid.uuid1().int)
        self.json_args['key'] = k
        yield self.application.db.insert(bucket, self.json_args)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(self.json_args)
