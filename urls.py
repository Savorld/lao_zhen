# -*- coding:utf-8 -*-

import config

from handlers.BaseHandler import StaticFileHandler
from handlers.Handlers import *
handlers = [
    (r'/', IndexHandler),
    (r'/intoClass(\d)-(_?\d+)', IntoClassHandler),
    (r'/api/shq/info', ShqInfoHandler),
    (r'/api/qy/info', QyInfoHandler),
    (r'/api/dx/info', DxInfoHandler),
    (r'/api/date/info', DateInfoHandler),
    (r'/(.*)', StaticFileHandler,
     dict(path=config.settings['static_path'], default_filename='index.html'))
]
