# -*- coding:utf-8 -*-
from scrapy.cmdline import execute

import sys
import os
__author__ = 'brynao'
__date__ = '2017/11/2 下午11:09'

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "car_spider"])