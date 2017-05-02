# coding: UTF-8

# 获取代理的类http://www.youdaili.net/
import re
import threading
import requests
from Utils.Logger import Logger

logger = Logger(__file__).getLogger()

rawProxyList = []

urls = []

urls.append("http://www.youdaili.net/Daili/")
urls.append("http://www.youdaili.net/Daili/http/")
urls.append("http://www.youdaili.net/Daili/guonei/")
urls.append("http://www.youdaili.net/Daili/guowai/")


# 获取代理的类
class ProxyByYoudaili(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.rawProxyList = rawProxyList

    def getProxy(self, target):
        # 获取当天发布的代理
        logger.info("[youdaili]代理服务器目标网站：%s", target)
        response = requests.get(target)
        txt = response.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(response.text)[0])
        pattern = re.compile('<div.*?class="cont_font".*?>.*?<div.*?class="cont_ad".*?>.*?<p>(.*?)</p>.*?</div>', re.S)
        txt = txt.replace("@HTTP#", ":")
        items = re.findall(pattern, txt)
        if (len(items) > 0):
            matchs = items[0].split("<br />\r\n")
            for match in matchs:
                ipdata = match.split(":")
                if (len(ipdata) > 1):
                    self.rawProxyList.append((ipdata[0], ipdata[1]))

    def getUrl(self, url):
        response = requests.get(url)
        txt = response.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(response.text)[0])
        pattern = re.compile(
            '<ul.*?class="newslist_line".*?>.*?<li.*?>.*?<a.*?href="(.*?)".*?target.*?>.*?</a>.*?</li>.*?</ul>', re.S)
        items = re.findall(pattern, txt)
        for item in items:
            if (item.encode("utf-8") != "http://www.youdaili.net/Daili/" and item.encode("utf-8") != "/"):
                url = item.encode("utf-8")
                self.getProxy(url)
                url = url.replace(".html", "_2.html")
                self.getProxy(url)

    def run(self):
        for url in urls:
            self.getUrl(url)
