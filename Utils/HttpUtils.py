# coding: UTF-8
import requests

# response.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(response.text)[0])
from requests.exceptions import ConnectionError

from Utils.Logger import Logger

_user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
_referer = "http://weixin.sogou.com"

logger = Logger(__file__).getLogger()


class HttpUtils():
    timeout = 6

    def __init__(self, proxies=None):
        self.proxies = proxies

    # 获取页面
    def getRedirctUrl(self, url, cookies):
        head = ""
        try:
            r = requests.head(url, cookies=cookies, proxies=self.proxies, timeout=self.timeout)
            head = r.headers.get("Location")
        except Exception, e:
            logger.warn("HttpUtils Exception: Error:%s ,Type:%s" % (e, type(e)))
        return head

    # 附带cookie跳转
    def gotoUrlWithCookie(self, url, cookie):
        content = ""
        try:
            headers = {"User-Agent": _user_agent, "Referer": _referer}
            r = requests.get(url, headers=headers, cookies=cookie, proxies=self.proxies, timeout=self.timeout)
            if (r.status_code == 200):
                content = r.text
        except Exception, e:
            logger.warn("HttpUtils Exception: Error:%s ,Type:%s" % (e, type(e)))
        return content

    # 获取cookie
    def getCookie(self, url):
        headers = {"User-Agent": _user_agent, "Referer": _referer}
        r = requests.head(url, headers=headers, proxies=self.proxies, timeout=self.timeout)
        return r.cookies
