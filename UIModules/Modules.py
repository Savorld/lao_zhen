# -*- coding:utf-8 -*-

from tornado.web import UIModule
from tornado import gen
from utils.DB import Pg_db
import config

class FooterModule(UIModule):

    # TODO:coroutine
    def render(self):
        pg = Pg_db()
        footer_cla = pg.query('select c_name from js_classes where '
                                   'c_level=2')
        return self.render_string('modules/footer.html', footer_cla=footer_cla)
class SubClassModule(UIModule):

    def render(self, cla_name):
        return self.render_string('modules/sub_class_name.html',
                                  cla_name=cla_name)