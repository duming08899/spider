# coding: UTF-8
from multiprocessing.pool import ThreadPool
import re
import time
import threadpool
from Model import Sy58

from Utils import WeiXin
from Utils.Logger import Logger

logger = Logger(__file__).getLogger()

if __name__ == "__main__":
    print 1

    Sy58.run();
