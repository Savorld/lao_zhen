# -*- coding:utf-8 -*-

import json

from tornado.web import RequestHandler, StaticFileHandler

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

    # def set_default_headers(self):
    #     self.set_header('Content-Type', 'application/json; charset=UTF-8')

    # def get_current_user(self):

class StaticFileHandler(StaticFileHandler):

    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token
