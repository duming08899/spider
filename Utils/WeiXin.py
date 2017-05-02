# coding:utf-8
import os

import random, time
import requests
from Config import Configs
from Utils.HttpUtils import HttpUtils
from Utils.Logger import Logger

logger = Logger(__file__).getLogger()


# 随机获取cookie
def process_cookie():
    # 数据初始化
    cookiesTxt = Configs.COOKIE_SET
    if len(cookiesTxt) == 0:
        logger.info("加载cookie文件... ")
        f = open(Configs.COOKIE_TXT_PATH)
        line = f.readline()
        while line:
            cookiesTxt.append(line)
            line = f.readline()
        f.close()
        Configs.COOKIE_SET = cookiesTxt

    maxRange = len(cookiesTxt)
    ##格式化
    cookieLine = cookiesTxt[random.randint(1, maxRange - 1)]
    cookieChars = cookieLine.split(",")
    cookie = "{'ABTEST':'{ABTEST}','SNUID':'{SNUID}','IPLOC':'{IPLOC}','SUID':'{SUID}','SUV':'{SUV}'}"
    cookie = cookie.replace("{ABTEST}", cookieChars[0])
    cookie = cookie.replace("{IPLOC}", cookieChars[1])
    cookie = cookie.replace("{SNUID}", cookieChars[2])
    cookie = cookie.replace("{SUID}", cookieChars[3])
    cookie = cookie.replace("{SUV}", cookieChars[4])
    return eval(cookie)


##获取新的cookie写入数据库中
def writeSogouCookie():
    SUV = HttpUtils().getCookie(Configs.WEIXIN_COOKIE_SUV)._find("SUV")
    OtherCookie = requests.get(Configs.WEIXIN_COOKIE_URL.format(q=time.time()), cookies={"SUV": SUV}).cookies
    ABTEST = OtherCookie._find("ABTEST")
    IPLOC = OtherCookie._find("IPLOC")
    SNUID = OtherCookie._find("SNUID")
    SUID = OtherCookie._find("SUID")
    cookieStr = ABTEST + "," + IPLOC + "," + SNUID + "," + SUID + "," + SUV + ","
    output = open(Configs.COOKIE_TXT_PATH, 'a')
    output.write("\n")
    output.write(cookieStr)
    output.close()
    logger.info("同步更新cookie文件 " + cookieStr)


def updateCookieFile(num):
    # 初始化cookie文件
    logger.info("同步更新cookie文件")
    output = open(Configs.COOKIE_TXT_PATH, 'w+')
    output.write("ABTEST,IPLOC,SNUID,SUID,SUV")
    output.close()
    # 写入cookie
    for i in range(1, num):
        time.sleep(3)
        writeSogouCookie()
