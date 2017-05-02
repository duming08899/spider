# coding: UTF-8
import random
import threading
import urllib2

import time
from Proxy.ProxyByKuaidaili import ProxyByKuaidaili
from Proxy.ProxyByXici import ProxyXici
from Proxy.ProxyByYoudaili import ProxyByYoudaili
from Proxy.ProxyIp002 import ProxyByIp002
from Utils import RedisUtils
from Utils.Logger import Logger

logger = Logger(__file__).getLogger()

rawProxyList = []
checkedProxyList = []
getThreads = []
ips = []


# 检验代理的类
class ProxyCheck(threading.Thread):
    def __init__(self, proxyList):
        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout = 5
        self.testUrl = "http://weixin.sogou.com/"
        self.testStr = "一搜即达"

    def checkProxy(self):
        RedisUtils.flush()
        cookies = urllib2.HTTPCookieProcessor()
        for proxy in self.proxyList:
            proxyHandler = urllib2.ProxyHandler({"http": r'http://%s:%s' % (proxy[0], proxy[1])})
            opener = urllib2.build_opener(cookies, proxyHandler)
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            t1 = time.time()
            try:
                req = opener.open(self.testUrl, timeout=self.timeout)
                result = req.read()
                timeused = time.time() - t1
                pos = result.find(self.testStr)
                if pos > 1 and int(timeused) < 20:
                    checkedProxyList.append((proxy[0], proxy[1], timeused))
                    RedisUtils.set("ip1-%s" % proxy[0], proxy[0] + ":" + proxy[1])
                    logger.info("ip %s" % proxy[0])
                else:
                    continue
            except Exception, e:
                continue

    def run(self):
        self.checkProxy()


# 搜集代理
def getProxyProcess():
    xici = ProxyXici()
    youdaili = ProxyByYoudaili()
    kuaidaili = ProxyByKuaidaili()
    ip002 = ProxyByIp002()
    getThreads.append(xici)
    getThreads.append(youdaili)
    getThreads.append(kuaidaili)
    getThreads.append(ip002)

    for i in range(len(getThreads)):
        getThreads[i].start()

    for i in range(len(getThreads)):
        getThreads[i].join()

    rawProxyList.extend(xici.rawProxyList)
    rawProxyList.extend(youdaili.rawProxyList)
    rawProxyList.extend(kuaidaili.rawProxyList)
    rawProxyList.extend(ip002.rawProxyList)
    ips = list(set(rawProxyList))
    logger.info('.' * 10 + "总共抓取了%s个代理" % len(ips) + '.' * 10)

    # 多线程校验
    checkThreads = []
    for i in range(20):
        t = ProxyCheck(ips[((len(ips) + 19) / 20) * i:((len(ips) + 19) / 20) * (i + 1)])
        checkThreads.append(t)

    for i in range(len(checkThreads)):
        checkThreads[i].start()

    for i in range(len(checkThreads)):
        checkThreads[i].join()

    print '.' * 10 + "总共有%s个代理通过校验" % len(checkThreads) + '.' * 10


if __name__ == "__main__":
    getProxyProcess()
