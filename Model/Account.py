# coding: UTF-8
import re
import threading
import threadpool
from Utils import DBUtils
from Utils import WeiXin
from Utils.HttpUtils import HttpUtils
from Utils.Logger import Logger
from Config import Configs
from Utils.ProxyProcess import process_proxy

logger = Logger(__file__).getLogger()

testStr = "<title></title>"


##根据关键字搜索公众账号
def handlePublicAccount(args):
    keyword = args[0]
    currentPage = args[1]
    accountType = args[2]

    items = parseAccount(keyword, currentPage)
    if (items is None):
        logger.warn("获取账号失败: %s" % keyword)
        return
    for item in items:
        openId = item[0]
        ext = item[1]
        logo = item[2]
        name = item[3]
        name = name.replace("<em><!--red_beg-->", "")
        name = name.replace("<!--red_end--></em>", "")

        account = item[4]
        account = account.encode("utf-8")
        account = account.replace("微信号：", "")

        rows = getRecByOpenId(openId)
        count = len(rows)
        if count == 0:
            sql = "insert into wd_public_account (account, name, openid, ext, logo, type, create_time) values("
            sql = sql + "\"" + account + "\",\"" + name + "\",\"" + openId + "\",\"" + ext + "\"," + "\"" + logo + "\"," + str(
                accountType) + ",sysdate())"
            logger.info("公众号更新:[新增]" + account + " 名称：" + name.encode("utf-8"))
            DBUtils.excute(sql)
        else:
            if rows[0][4] <> ext:
                sql = "update wd_public_account set ext=" + "\"" + ext + "\",update_time=sysdate() where account=" + "\"" + account + "\""
                logger.info("公众号更新:[更新]" + account + " 名称：" + name.encode("utf-8"))
                DBUtils.excute(sql)


# 解析HTML
def parseAccount(keyword, currentPage):
    link = Configs.WEIXIN_GZH_URL.format(key=keyword, pageNo=str(currentPage))
    try:
        page = HttpUtils(process_proxy()).gotoUrlWithCookie(link, WeiXin.process_cookie())
        if page == "":
            logger.warn("HttpUtils异常: %s" % (link))
            return []
        pos = page.find(testStr)
        if pos > 1:
            logger.warn("Sogou拒绝访问: %s" % (link))
            return []

        # 分析页面
        pre = re.compile(
            '<div.*?class="wx-rb.*?_item".*?href="/gzh\\?openid=(.*?)&amp;ext=(.*?)".*?target="_blank".*?>.*?' +
            '<div.*?class="img-box">.*?<span class="ico-bg"></span>.*?<img.*?src="(.*?)".*?onload=.*?</div>.*?' +
            '<div.*?class="txt-box.*?<h3>(.*?)</h3>.*?<h4>.*?<span>(.*?)</span>.*?</h4>.*?</div>', re.S)
        items = re.findall(pre, page)
        logger.info("解析页面成功:" + link)
        return items
    except Exception, e:
        logger.warn("解析页面异常: %s ERROR：%s" % (link, e))


# 通过账号获取
def getRecByOpenId(openid):
    rows = DBUtils.query("select * from wd_public_account where openid='" + openid + "'");
    return rows


# 获取所有账号
def getAllAccount():
    rows = DBUtils.query("select * from wd_public_account");
    return rows


def run(args):
    pool = threadpool.ThreadPool(5)
    requests = threadpool.makeRequests(handlePublicAccount, args)
    [pool.putRequest(req) for req in requests]
    pool.wait()
