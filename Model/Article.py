# coding: UTF-8
import random
import re
import threading
import time
from xml.dom.minidom import parseString
import threadpool

from Utils.HttpUtils import HttpUtils
from Utils import DBUtils
from Utils.Logger import Logger
from Utils import WeiXin
from Config import Configs
from Utils.ProxyProcess import process_proxy, removeIp, delIp

logger = Logger(__file__).getLogger()

testStr = "antispider"


# 根据公众号获取其微信文章
def parseArticleWithAccount(args):
    openid = args[0]
    ext = args[1]
    currentPage = args[2]
    account = args[3]

    t = str(int(time.time())) + str(random.randint(100, 999))
    cookie = WeiXin.process_cookie()  # 根据cookie获取文章
    proxy = process_proxy()  # 获取代理

    url = Configs.WEIXIN_ART_URL.format(openid=openid, ext=ext, pageno=currentPage, t=t)  # 根据公众号获取文章
    logger.info("获取公众号文章,账号名称:%s page %s" % (account.encode("utf-8"), currentPage))
    page = HttpUtils(proxy).gotoUrlWithCookie(url, cookie)
    # 连接异常
    if len(page) == 0 or page is None:
        delIp(proxy)
        return "stop"


    ##判断是否非法请求
    pos = page.find(testStr)
    if pos > 1:
        logger.info("获取公众号文章Sogou拒绝访问: IP %s %s %s" % (proxy, account.encode("utf8"), url))
        removeIp(proxy)
        return "stop"


    # 解析文章
    page = page.replace("\\", "")
    page, number = re.subn("<\?xml version=.*?encoding=.*?>", "", page)
    page, number = re.subn("sogou.weixin.gzhcb.*?items\":\[\"", "", page)
    end = page.find("\"]})")
    page = page[0:end]
    page = "<wx>" + page + "</wx>"
    page = page.encode("utf-8")

    try:
        doc = parseString(page)
    except Exception, Argument:
        logger.warn("解析文章数据错误 IP:%s %s" % (Argument, page))
        removeIp(proxy)
        return "stop"

    documents = doc.documentElement.getElementsByTagName("DOCUMENT")
    for document in documents:
        status = "0"
        item = document.getElementsByTagName('item')[0]
        display = item.getElementsByTagName("display")[0]
        article_title = display.getElementsByTagName('title')[0].childNodes[0].data  # 文章标题',
        article_url = display.getElementsByTagName('url')[0].childNodes[0].data  # 文章地址',

        proxy = process_proxy()
        article_url_real = HttpUtils(proxy).getRedirctUrl(Configs.WEIXIN_HOST.format(key=article_url), cookie)
        if (article_url_real is None or len(article_url_real) == 0 or article_url_real.find("antispider") > 0):
            logger.warn("换取微信地址异常，Sogou拒绝 %s %s" % (proxy, article_url_real))
            removeIp(proxy)
            continue

        article_head = display.getElementsByTagName('imglink')[0].childNodes[0].data  # 图片',
        account_name = display.getElementsByTagName('sourcename')[0].childNodes[0].data  # 公众号名称',
        account_logo = display.getElementsByTagName('headimage')[0].childNodes[0].data  # 公众号LOGO',
        openid = display.getElementsByTagName('openid')[0].childNodes[0].data  # 公众账号',
        ext = display.getElementsByTagName('ext')[0].childNodes[0].data  # 扩展请求',
        doc_id = display.getElementsByTagName('docid')[0].childNodes[0].data  # 文章ID
        tpl_id = item.getElementsByTagName('tplid')[0].childNodes[0].data  # 类型ID',
        class_id = item.getElementsByTagName('classid')[0].childNodes[0].data  # 等级ID
        lastModified = item.getElementsByTagName('lastModified')[0].childNodes[0].data  # 等级ID
        lastModifiedTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(lastModified)))

        # 文章入库
        sql = "insert into wd_article (article_title, article_url, article_head, article_desc, account_name, account_logo, openid, ext, doc_id, tpl_id, class_id,create_time,publish_time,status ) values ("
        sql = sql + "\"" + article_title + "\",\"" + article_url_real + "\",\"" + article_head + "\",\"" + "--" + "\",\"" + account_name + "\",\"" + account_logo + "\",\"" + openid + "\",\"" + ext + "\",\"" + doc_id + "\"," + tpl_id + "," + class_id + ",sysdate(),str_to_date('" + lastModifiedTime + "','%Y-%m-%d %H:%i:%s')," + status + ")"
        logger.info("【新增】公众号文章【" + (account_name.encode('utf-8')) + "】 ,【标题】=" + (article_title.encode('utf-8')))
        DBUtils.excute(sql)


def run(args):
    pool = threadpool.ThreadPool(5)
    requests = threadpool.makeRequests(parseArticleWithAccount, args)
    [pool.putRequest(req) for req in requests]
    pool.wait()
