# -*- coding:utf-8 -*-

import json
import logging

from tornado.web import RequestHandler, StaticFileHandler
from tornado import gen

class BaseHandler(RequestHandler):

    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def prepare(self):
        self.xsrf_token
        if self.request.headers.get('Content-Type', '').startswith(
                'application/json'):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = {}

    @gen.coroutine
    def query(self, sql, *args):
        ret = []
        # print 'sql=', sql
        # print 'args=', args
        try:
            if args:
                cursor = yield self.db.execute(sql, *args)
            else:
                cursor = yield self.db.execute(sql, None)
            _fetch = cursor.fetchall()
            # _fetch = map(lambda x: tuple(x.values()), fetch)
            # print '_fetch=', _fetch
            if _fetch:
                ret = _fetch
        except Exception as e:
            logging.error(e)
        finally:
            raise gen.Return(ret)


    # def set_default_headers(self):
    #     self.set_header('Content-Type', 'application/json; charset=UTF-8')

    # def get_current_user(self):

class StaticFileHandler(StaticFileHandler):

    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token
