# coding: UTF-8

# 获取代理的类http://www.ip002.com/free.html
import re
import threading
from Utils.Logger import Logger
from Utils.HttpUtils import HttpUtils

logger = Logger(__file__).getLogger()

rawProxyList = []

url = "http://www.ip002.com/free.html"


class ProxyByIp002(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.rawProxyList = rawProxyList

    def getProxy(self, target):
        logger.info("【ip002】代理服务器目标网站：%s", target)
        txt = HttpUtils().gotoUrlWithCookie(target, [])
        txt = txt.encode("utf-8")
        pattern = re.compile('<tr>(.*?)</tr>', re.S)
        items = re.findall(pattern, txt)
        items = items[2:]
        for item in items:
            pattern = re.compile('<td.*?>(.*?)</td>', re.S)
            tds = re.findall(pattern, item)
            if (len(tds) > 2):
                self.rawProxyList.append((tds[0], tds[1]))

    def run(self):
        self.getProxy(url)
