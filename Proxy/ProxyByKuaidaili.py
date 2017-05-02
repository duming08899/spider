# coding: UTF-8

# 获取代理的类http://www.kuaidaili.com/proxylist/10/
import re
import threading
from Utils.Logger import Logger
from Utils.HttpUtils import HttpUtils

logger = Logger(__file__).getLogger()

rawProxyList = []

urls = []
urls.append("http://www.kuaidaili.com/proxylist/{page}/")
urls.append("http://www.kuaidaili.com/free/inha/{page}/")
urls.append("http://www.kuaidaili.com/free/intr/{page}/")
urls.append("http://www.kuaidaili.com/free/outha/{page}/")
urls.append("http://www.kuaidaili.com/free/outtr/{page}/")


class ProxyByKuaidaili(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.rawProxyList = rawProxyList

    def getProxy(self, target):
        logger.info("【KDL】代理服务器目标网站：%s", target)
        txt = HttpUtils().gotoUrlWithCookie(target, [])
        txt = txt.encode("utf-8")
        pattern = re.compile('<tr>(.*?)</tr>', re.S)
        items = re.findall(pattern, txt)
        for item in items:
            pattern = re.compile('<td>(.*?)</td>', re.S)
            tds = re.findall(pattern, item)
            if (len(tds) > 2):
                self.rawProxyList.append((tds[0], tds[1]))

    def run(self):
        for url in urls:
            for i in range(1, 6):
                self.getProxy(url.format(page=i))
