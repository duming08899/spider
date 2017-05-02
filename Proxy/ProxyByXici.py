# coding: UTF-8

# 获取代理的类www.xicidaili.com
import re
import threading
from Utils.Logger import Logger
from Utils.HttpUtils import HttpUtils

logger = Logger(__file__).getLogger()

rawProxyList = []
urls = []
urls.append("http://www.xicidaili.com/nt/{page}")
urls.append("http://www.xicidaili.com/nn/{page}")
urls.append("http://www.xicidaili.com/nn/{page}")
urls.append("http://www.xicidaili.com/wn/{page}")
urls.append("http://www.xicidaili.com/wt/{page}")


class ProxyXici(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.rawProxyList = rawProxyList

    def getProxy(self, target):
        logger.info("【xici】代理服务器目标网站：%s", target)
        txt = HttpUtils().gotoUrlWithCookie(target, [])
        txt = txt.encode("utf-8")
        pattern = re.compile('<tr.*?>(.*?)</tr>', re.S)
        items = re.findall(pattern, txt)
        tdpattern = re.compile('<td.*?>(.*?)</td>', re.S)
        for item in items:
            tds = re.findall(tdpattern, item)
            if (len(tds) > 4):
                print tds[1] + " " + tds[2]
                self.rawProxyList.append((tds[1], tds[2]))

    def run(self):
        for url in urls:
            for i in range(1, 6):
                self.getProxy(url.format(page=i))
