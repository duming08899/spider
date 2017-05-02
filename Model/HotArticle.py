# http://weixin.sogou.com/pcindex/pc/pc_0/1.html
# coding: UTF-8

import random
import re
import threading
import time
from Config import Configs
from Model.Account import Account
from Utils import WeiXin
from Utils.HttpUtils import HttpUtils
from Utils.Logger import Logger
from Utils import DBUtils

import sys
from Utils.ProxyProcess import process_proxy

reload(sys)
sys.setdefaultencoding('utf-8')

logger = Logger(__file__).getLogger()


class HotArticle(threading.Thread):
    def __init__(self, pageNo):
        threading.Thread.__init__(self)
        self.pageNo = pageNo

    def parseIndexHotArt(self):
        # 时间戳
        timestamp = int(time.time())
        randomNum = random.randint(100, 999)
        t = str(timestamp) + str(randomNum)
        # 根据cookie获取文章
        cookie = WeiXin.process_cookie()
        # 获取代理
        proxy = process_proxy()
        # 根据公众号获取文章
        url = Configs.WEIXIN_HOT_ART.format(pageNo=self.pageNo)
        page = HttpUtils(proxy).gotoUrlWithCookie(url, cookie)
        page = page.encode('ISO-8859-1').decode("utf-8")
        pre = re.compile('<li.*?id="(.*?)".*?>.*?'+
                         '<div.*?>.*?<img.*?src="(.*?)".*?">.*?</div>.*?'+
                         '<div.*?>.*?<a.*?href=".*?openid=(.*?)&ext=(.*?)".*?>.*?<p>.*?<img.*?src="(.*?)".*?</p>.*?<p.*?title="(.*?)">.*?</p>.*?</a>.*?</div>.*?'+
                         '<div.*?>.*?<h4>.*?<a.*?href="(.*?)".*?>(.*?)</a>.*?</h4>.*?</div>.*?'
                         '</li>',re.S)
        items = re.findall(pre, page)
        for item in items:
            doc_id =item[0]
            account_logo=item[4]
            openid =item[2]
            ext =item[3]
            article_head=item[1]
            account_name=item[5]
            article_url=item[6]
            article_title=item[7]
            article_desc=""
            # 文章入库
            sql = "insert into wd_article_hot (article_title, article_url, article_head, article_desc, account_name, account_logo, openid, ext,doc_id, create_time ) values ("
            sql = sql + "\"" + article_title + "\",\"" + article_url + "\",\"" + article_head + "\",\"" + "--" + "\",\"" + account_name + "\",\"" + account_logo + "\",\"" + openid + "\",\"" + ext + "\",\""+doc_id+"\","+"sysdate())"
            logger.info("【新增】首页热门文章【" + (account_name.encode('utf-8')) + "】 ,【标题】=" + (article_title.encode('utf-8')))
            DBUtils.excute(sql)

            #新增账号
            account="testing"
            accountType=0
            rows = Account().getRecByOpenId(openid)
            count = len(rows)
            if count == 0:
                sql = "insert into wd_public_account (account, name, openid, ext, logo, type, create_time) values("
                sql = sql + "\"" + account + "\",\"" + account_name + "\",\"" + openid + "\",\"" + ext + "\"," + "\"" + account_logo + "\"," + str(accountType) + ",sysdate())"
                logger.info("公众号更新:[新增]" + account + " 名称：" + account_name.encode("utf-8"))
                DBUtils.excute(sql)
            else:
                if rows[0][4] <> ext:
                    sql = "update wd_public_account set ext=" + "\"" + ext + "\",update_time=sysdate() where account=" + "\"" + account + "\""
                    logger.info("公众号更新:[更新]" + account + " 名称：" + account_name.encode("utf-8"))
                    DBUtils.excute(sql)

    def run(self):
        self.parseIndexHotArt()
