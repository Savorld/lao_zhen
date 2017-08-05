# -*- coding:utf-8 -*-

from tornado.web import UIModule
from utils.DB import Pg_db
import config

class FooterModule(UIModule):

    def render(self):
        pg = Pg_db()
        footer_cla = pg.query('select c_name from js_classes where '
                                   'c_level=2')
        return self.render_string('modules/footer.html', footer_cla=footer_cla)