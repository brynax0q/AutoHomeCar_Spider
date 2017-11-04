# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # str 北京奔驰-奔驰C级
    url = scrapy.Field()   # str
    score = scrapy.Field() # str 4.32
    comment_nums = scrapy.Field()  # int 394
    groups = scrapy.Field()
    # dict {'款式':'价格'}
    comments = scrapy.Field()


