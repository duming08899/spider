# coding: UTF-8
# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
import logging
from Config.Configs import LOG_FILE_PATH


class Logger():
    _logname = LOG_FILE_PATH

    def __init__(self, logger):
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(Logger._logname)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(levelname)s %(asctime)s %(module)s.%(funcName)s %(lineno)d: %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getLogger(self):
        return self.logger
