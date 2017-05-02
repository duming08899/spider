# coding: UTF-8
# 获取代理
import random
import time
from Utils import RedisUtils
from Utils.Logger import Logger

logger = Logger(__file__).getLogger()


def process_proxy():
    currentKey = getIpstate();
    key = "ip%s-" % currentKey
    keys = RedisUtils.getKeys(key)
    keyNum = len(keys)
    if (keyNum < 1):
        logger.info("代理池异常数量<1 sleepping 120s")
        RedisUtils.set("ipstate", int(currentKey) + 1)
        time.sleep(1200)
        key = "ip%s-" % getIpstate()
        keys = RedisUtils.getKeys(key)
        keyNum = len(keys)

    randNum = random.randint(0, keyNum - 1)
    current = keys[randNum]
    value = RedisUtils.get(current)
    proxies = {}
    proxies["http"] = r'http://%s' % value
    removeIp(proxies)
    return proxies


def removeIp(ip):
    if (ip and len(ip) > 0):
        value = ip.get("http")
        value = value.replace("http://", "")
        nPos = value.index(":")
        if (nPos > 0):
            ip = value[0:nPos]
            RedisUtils.remove("ip%s-%s" % (getIpstate(), ip))
            ipstate = int(getIpstate()) + 1
            RedisUtils.set("ip%s-%s" % (ipstate, ip), value)


def delIp(ip):
    if (ip and len(ip) > 0):
        value = ip.get("http")
        value = value.replace("http://", "")
        nPos = value.index(":")
        if (nPos > 0):
            ip = value[0:nPos]
            ipstate = int(getIpstate()) + 1
            RedisUtils.remove("ip%s-%s" % (ipstate, ip))
            logger.info("删除代理ip %s-%s" % (ipstate, ip))


def getIpstate():
    ipstate = RedisUtils.get("ipstate")
    if (ipstate):
        return "%s" % ipstate
    else:
        RedisUtils.set("ipstate", 1)
        return "1"
