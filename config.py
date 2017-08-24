# -*- coding:utf-8 -*-

import os
from UIModules.Modules import  *

log_level = 'debug'
log_file = os.path.join(os.path.dirname(__file__), 'logs', 'log')

settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'template'),
    'cookie_secret': "kb8LwR4MSASQzT+HWLqy4YWnN1DJcEKJrjblnr77uSw=",
    'xsrf_cookies': True,
    'debug': True,
    'ui_modules': dict(Footer=FooterModule, SubCla=SubClassModule)
    # 'compiled_template_cache': False,
    # 'autoescape': None,
    # 'login_url': '/login',
}



# pg_options = dict(
#     database = 'laozhen',
#     user = 'dbuser',
#     password = 'wyc123',
#     host = '122.114.131.81',
#     port = 5432
# )

pg_options = dict(
    database = 'laozhen',
    user = 'postgres',
    password = 'wyc123',
    host = '45.78.52.25',
    port = 5432
)


redis_options = dict(
    host = '45.78.52.25',
    port = 6379
)