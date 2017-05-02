# coding: UTF-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import re
from Utils.HttpUtils import HttpUtils
from Utils.Logger import Logger
from Config import Configs

logger = Logger(__file__).getLogger()

testStr = "kkk"


# 搜索58同城催乳师页面
def handle58CRS():
    for num in range(1, 2):
        items = parseCRS(num)
        for item in items:
            print item
            print "-----"


# 解析HTML
def parseCRS(num):
    link = Configs.SY58CRS.format(num=num)
    try:
        page = HttpUtils().gotoUrlWithCookie(link, None)

        if page == "":
            logger.warn("HttpUtils异常: %s" % (link))
            return []
        pos = page.find(testStr)
        if pos > 1:
            logger.warn("58拒绝访问: %s" % (link))
            return []

        # 分析页面
        pre = re.compile('<tr.*?logr=.*?>.*?<td class="t".*?>.*?href="(.*?)".*?target.*?</td>.*?</tr>', re.S)
        items = re.findall(pre, page)
        logger.info("解析页面成功:" + link)
        return items
    except Exception, e:
        logger.warn("解析页面异常: %s ERROR：%s" % (link, e))


if __name__ == "__main__":
    handle58CRS()
