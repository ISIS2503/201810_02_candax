# -*- coding: utf-8 -*-

import riak
import functools
import tornado.gen
import logging
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

MAX_WORKERS = 10
LOGGER = logging.getLogger(__name__)


def threadexecute(f):
    @functools.wraps(f)
    @tornado.gen.coroutine
    def wrapper(self, *args, **kwargs):
        resp = yield self.executor.submit(f, self, *args, **kwargs)
        return resp
    return wrapper


class RiakDB:
    instance = None

    def __init__(self, riak_url):
        url = urlparse(riak_url)
        self.client = riak.RiakClient(
            protocol=url.scheme, host=url.hostname, pb_port=url.port,
            http_port=url.port)
        self.executor = ThreadPoolExecutor(MAX_WORKERS)

    @threadexecute
    def insert(self, bucket, d):
        bucket = self.client.bucket(bucket)
        obj = bucket.new(d['key'], data=d)
        obj.store()
        return d

    @threadexecute
    def get_all(self, bucket):
        bucket = self.client.bucket(bucket)
        return [bucket.get(key).data for key in bucket.get_keys()]

    @threadexecute
    def get(self, bucket, key):
        bucket = self.client.bucket(bucket)
        return bucket.get(key).data

    @threadexecute
    def update(self, bucket, d):
        bucket = self.client.bucket(bucket)
        obj = bucket.get(d['key'])
        obj.data = d
        obj.store()
        return bucket.get(d['key']).data

    @threadexecute
    def delete(self, bucket, key):
        bucket = self.client.bucket(bucket)
        obj = bucket.get(key)
        ret = obj.data
        obj.delete()
        return ret

#    Propietario: request_id = res_unit; houseX
#    Admin: request_id = res_unitX
    @threadexecute
    def get_all_user(self, bucket, request_id, type):
        bucket = self.client.bucket(bucket)
        ret = []
        parts = request_id.split(';')
        for key in bucket.get_keys():
            act = bucket.get(key).data
            print(act['res_unit'])
            print(act['house'])
            if type == 'Admin' and act['res_unit'] == parts[0]:
                ret.append(act)
            elif type == 'Owner' and act['res_unit'] == parts[0] and act['house'] == parts[1]:
                ret.append(act)
        return ret

    @threadexecute
    def get_neighborhood(self, bucket, bucket_RU, request_id):
        ret = []
        alarmsB = self.client.bucket(bucket)
        resUnits = self.client.bucket(bucket_RU)

        for key in alarmsB.get_keys():
            act = alarmsB.get(key).data
            for key in resUnits.get_keys():
                act_RU = resUnits.get(key).data
                if act['res_unit']== act_RU['key'] and act_RU['Barrio'] == request_id:
                    ret.append(act)
        return ret

    @threadexecute
    def get_hour(self, bucket, request_id, type):
        ret = []
        alarmsB = self.client.bucket(bucket)
        for key in alarmsB.get_keys():
            act = alarmsB.get(key).data
            date = act['date']
            datetime_object = datetime.strptime(date, '%H:%M %d-%m-%Y')
            date_now = datetime.now()
            if act[type]== request_id and ((date_now - timedelta(hours = 1))<datetime_object):
                ret.append(act)
        return ret

    @threadexecute
    def get_month(self, bucket, request_id, type):
        ret = []
        alarmsB = self.client.bucket(bucket)
        month,year,search_by = request_id.split('/')
        print(year)
        print(month)
        print(search_by)
        search_date = datetime.strptime(month + '-' + year, '%m-%Y')

        for key in alarmsB.get_keys():
            act = alarmsB.get(key).data
            date = act['date']
            alarm_date = datetime.strptime(date, '%H:%M %d-%m-%Y')
            print(alarm_date.year==search_date.year)
            print(alarm_date.month==month)
            if act[type]==search_by and alarm_date.year==search_date.year and alarm_date.month==search_date.month:
                print('aaaa')
                ret.append(act)
        return ret
