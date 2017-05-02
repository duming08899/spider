# coding: UTF-8

# 项目路径
PROJECT_PATH = "D:\duming\weido"
# Cookie文件
COOKIE_TXT_PATH = PROJECT_PATH + "\Config\Cookie.txt"
# Proxy
PROXY_TXT_PATH = PROJECT_PATH + "\Config\Proxy.txt"
# LOG文件
LOG_FILE_PATH = PROJECT_PATH + "\logs\myapp.log"


# 搜索公众号
WEIXIN_GZH_URL = 'http://weixin.sogou.com/weixin?type=1&query={key}&ie=utf8&page={pageNo}'
# 公众号的文章
WEIXIN_ART_URL = 'http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid={openid}&ext={ext}&gzhArtKeyWord=&page={pageno}&t={t}'
# 获取cookie
WEIXIN_COOKIE_URL = 'http://weixin.sogou.com/weixin?query={q}'
# 获取SUV的地址
WEIXIN_COOKIE_SUV = 'http://pb.sogou.com/pb.js'
##微信文章
WEIXIN_HOST ='http://weixin.sogou.com/{key}'

##热门首页
WEIXIN_HOT_ART ='http://weixin.sogou.com/pcindex/pc/pc_0/{pageNo}.html'

# Cookie 内存
COOKIE_SET = []
# Proxy 内存
PROXY_SET = []
