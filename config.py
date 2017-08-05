# -*- coding:utf-8 -*-

import os
from UIModules.Modules import  FooterModule

log_level = 'debug'
log_file = os.path.join(os.path.dirname(__file__), 'logs', 'log')

settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'template'),
    'cookie_secret': "kb8LwR4MSASQzT+HWLqy4YWnN1DJcEKJrjblnr77uSw=",
    'xsrf_cookies': True,
    'debug': True,
    'ui_modules': {'Footer': FooterModule}
    # 'compiled_template_cache': False,
    # 'autoescape': None,
    # 'login_url': '/login',
}

# mysql_options = dict(
#     host = '',
#     database = '',
#     user = '',
#     password = ''
# )

pg_options = dict(
    database = 'laozhen',
    user = 'dbuser',
    password = 'wyc123',
    host = '122.114.131.81',
    port = 5432
)

redis_options = dict(
    host = '',
    port = 6379
)