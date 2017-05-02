import redis

from Config import Configs


def set(key, value):
    r = redis.Redis(host=Configs.REDIS_HOST, port=6379, db=12)
    r.set(key, value)


def get(key):
    r = redis.Redis(host=Configs.REDIS_HOST, port=6379, db=12)
    return r.get(key)


def getKeys(ip):
    r = redis.Redis(host=Configs.REDIS_HOST, port=6379, db=12)
    return r.keys(ip + "*")


def remove(key):
    r = redis.Redis(host=Configs.REDIS_HOST, port=6379, db=12)
    r.delete(key)


def flush():
    r = redis.Redis(host=Configs.REDIS_HOST, port=6379, db=12)
    r.flushdb()


def incr(key):
    r = redis.Redis(host=Configs.REDIS_HOST, port=6379, db=12)
    r.incr(key)
