# -*- coding:utf-8 -*-

from tornado.web import UIModule
from handlers.BaseHandler import BaseHandler
from tornado import gen
from utils.DB import Pg_db
import config

class FooterModule(UIModule):

    def render(self, footer_cla):
        return self.render_string('modules/footer.html',
                                       footer_cla=footer_cla)
class SubClassModule(UIModule):

    def render(self, cla_name):
        return self.render_string('modules/sub_class_name.html',
                                  cla_name=cla_name)