# coding: UTF-8
from Utils import DBUtils


def queryHotWord():
    rows = DBUtils.query("select * from hotword")
    return rows
