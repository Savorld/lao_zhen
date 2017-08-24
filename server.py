# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import redis
import config
import momoko
import datetime

from psycopg2.extras import RealDictCursor
from tornado.options import define, options
from tornado.web import Application
from urls import handlers
from utils.DB import Pg_db

define('port', type=int, default=3676, help='run server on the given port')

class Application(Application):

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.ioloop = tornado.ioloop.IOLoop.instance()
        # self.db = Pg_db(**config.pg_options)
        # momoko的pg异步库连接池
        dsn = 'dbname={database} user={user} password={password} host={host} ' \
              'port={port}'.format(
            **config.pg_options)
        self.db = momoko.Pool(
            dsn=dsn,
            cursor_factory=RealDictCursor,
            size=1,
            max_size=36,
            ioloop=self.ioloop,
            setsession=("SET TIME ZONE PRC",),
            raise_connect_errors=True,
            auto_shrink=True,
            shrink_delay=datetime.timedelta(seconds=10),
            shrink_period=datetime.timedelta(seconds=10)
        )
        future = self.db.connect()
        self.ioloop.add_future(future, lambda f: self.ioloop.stop())
        self.ioloop.start()
        future.result()

        self.redis = redis.StrictRedis(**config.redis_options)

def main():
    options.log_file_prefix = config.log_file
    tornado.options.parse_command_line()
    options.logging = config.log_level
    app = Application(
        handlers, **config.settings
    )
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    # http_server.start(0)
    app.ioloop.start()

if __name__ == '__main__':
    main()