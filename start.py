# coding: UTF-8
from multiprocessing.pool import ThreadPool
import re
import time
import threadpool
from Model import Account
from Model import Article
from Model.HotWord import queryHotWord
from Utils import WeiXin
from Utils.Logger import Logger

logger = Logger(__file__).getLogger()


# 同步更新账号
def getAccount():
    args = []
    words = queryHotWord()
    logger.info("同步【更新公众号】 热词数量:" + str(len(words)))
    for word in words:
        for i in range(1, 11):
            args.append([word[1], i, word[2]])
    Account.run(args)
    logger.info("同步【更新公众号】 热词数量:结束")


# 根据账号获取该账号前两页文章
def getArtByAccount():
    args = []
    rows = Account.getAllAccount()
    logger.info("同步【公众号文章】 公众号数:" + str(len(rows)))
    for row in rows:
        for i in range(1, 2):
            args.append([row[3], row[4], i, row[2]])
    Article.run(args)
    logger.info("同步【公众号文章】 结束")


if __name__ == "__main__":
    WeiXin.process_cookie()
    getArtByAccount()
