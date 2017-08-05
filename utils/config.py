# -*- coding:utf-8 -*-

import os

log_level = 'debug'
log_file = os.path.join(os.path.dirname(__file__), 'logs', 'log')

settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'template'),
    'cookie_secret': "kb8LwR4MSASQzT+HWLqy4YWnN1DJcEKJrjblnr77uSw=",
    'xsrf_cookies': True,
    'debug': True,
}

# mysql_options = dict(
#     host = '',
#     database = '',
#     user = '',
#     password = ''
# )

pg_options = dict(
    database = 'laozhen',
    user = 'postgres',
    password = 'wyc123',
    host = 'localhost',
    port = 5432
)

redis_options = dict(
    host = '',
    port = 6379
)