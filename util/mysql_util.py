# -*- coding:utf-8  -*-
import sys
sys.path.append("..")
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import MySQLdb
# from DBUtils.PooledDB import PooledDB
from settings import database
import logging as log
import time
class DataBaseUtil(object):
    def __init__(self):
        self.host = database['host']
        self.user = database['user']
        self.passwd = database['passwd']
        self.db = database['db']


    @classmethod
    def getConn(cls):
        conn = None
        is_false = True
        while is_false:
            try:
                conn = MySQLdb.connect(db=database['db'],host=database['host'],user=database['user'],passwd=database['passwd'],charset='utf8')
                is_false = False
            except:
                time.sleep(0.5)
        return conn

    @classmethod
    def execute(cls,sql):
        log.debug(sql)
        conn = cls.getConn()
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()

    @classmethod
    def select(cls,sql):
        conn = cls.getConn()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return result

if __name__ == '__main__':
    print 'start init '