# coding: UTF-8
import MySQLdb
from Utils.Logger import Logger

logger = Logger(__file__).getLogger()


def excute(str):
    try:
        conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', db="weido", port=3306, charset="utf8")
        cur = conn.cursor()
        cur.execute(str)
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        logger.warn("Mysql Error %d: %s" % (e.args[0], e.args[1]))


def query(str):
    try:
        conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', db="weido", port=3306, charset="utf8")
        cursor = conn.cursor()
        cursor.execute(str)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except MySQLdb.Error, e:
        logger.warn("Mysql Error %d: %s" % (e.args[0], e.args[1]))
