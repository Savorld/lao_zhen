# -*- coding:utf-8 -*-
import config
import logging

from psycopg2 import connect, extras
from tornado.gen import coroutine, Return

class Pg_db(object):

    def __init__(self, **kwargs):
        self.con = connect(**config.pg_options)
        self.cur = self.con.cursor()


    def query(self, sql, *args):
        ret = None
        try:
            self.cur.execute(sql, *args)
            fetch = self.cur.fetchall()
            if fetch:
                ret = fetch
            else:
                ret = []
        except Exception as e:
            logging.error(e)
        return ret

    def insert(self, sql, *args):
        try:
            self.cur.execute(sql, *args)
            self.con.commit()
            ret = 'ok'
        except Exception as e:
            logging.error(e)
            ret = 'error'
        return ret

    def __del__(self):
        self.con.close()

def test():
    con = connect(**config.pg_options)
    cur = con.cursor()
    cur.execute('SELECT * FROM lz_classes;')
    fet = cur.fetchall()
    print fet

def test1():
    p = Pg_db()

if __name__=='__main__':
    test()

