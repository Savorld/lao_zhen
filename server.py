# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import psycopg2
import redis
import config

from tornado.options import define, options
from tornado.web import Application
from urls import handlers
from utils.DB import Pg_db

define('port', type=int, default=3668, help='run server on the given port')

class Application(Application):

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.db = Pg_db(**config.pg_options)
        self.redis = redis.StrictRedis(**config.redis_options)

def main():
    options.logging = config.log_level
    options.log_file_prefix = config.log_file
    tornado.options.parse_command_line()
    app = Application(
        handlers, **config.settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    # http_server.start(0)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()