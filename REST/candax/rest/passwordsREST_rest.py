
import json
import logging
import tornado.web
import tornado.escape
import tornado.httpclient as httpclient
from requests import post as posty
import candax.rest as rest
from candax.auth import jwtauth

LOGGER = logging.getLogger(__name__)
bucket = 'passwords'


# alarm = {'house': ; 'res_unit': ; 'hub': ; 'lock': ; 'date':}
@jwtauth
class MainHandler(rest.BaseHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def get(self, _, _id=None):
        # print("MSG: {0}".format(self.application.db is None))
        if _id is None:
            objs = yield self.application.db.get_all(bucket)
        else:
            objs = yield self.application.db.get(bucket, _id)
        # self.set_status(403)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        print(self.json_args)
        client = httpclient.AsyncHTTPClient()
        h = {'Content-Type': 'application/json; charset=UTF-8'}
        request = httpclient.HTTPRequest(url='http://localhost:5000/pwds',
                                         method='POST',
                                         body=json.dumps(self.json_args),
                                         headers=h)
        # try:
        print(self.json_args)
        response = client.fetch(request)
        # except Exception as ex:
        #     raise ex
        # print("posteando....")
        # posty('http://172.24.42.47:5000/pwds', json=self.json_args)
        # print("posteado.")
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(self.json_args)

    @tornado.gen.coroutine
    def put(self, *args):
        # print("MSG: {0}".format(self.application.db is None))
        # bucket = 'test'
        objs = yield self.application.db.update(bucket, self.json_args)
        # self.set_status(403)
        print(objs)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)

    @tornado.gen.coroutine
    def delete(self, _, _id=None):
        # bucket = 'test'
        print(_id)
        if _id is None:
            # objs = yield self.application.db.get_all(bucket)
            print('no hay naditaaaaa')
        else:
            objs = yield self.application.db.delete(bucket, _id)
        # self.set_status(403)
        objs = json.dumps(objs)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(objs)
