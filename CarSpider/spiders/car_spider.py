# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request

from CarSpider.items import CarspiderItem

class CarSpiderSpider(scrapy.Spider):
    headers = {
        "HOST": "www.autohome.com.cn/",
        "Referer": "https://www.autohome.com.cn",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }
    name = 'car_spider'
    allowed_domains = ['www.autohome.com.cn/']
    start_urls = []
    chars = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y','Z']
    #chars = ['A']
    for char in chars:
        root_url = "http://www.autohome.com.cn/grade/carhtml/" + char + ".html"
        start_urls.append(root_url)

    # 在每一个汽车列表页中提取每个汽车的url并交给 parse_detail 解析
    def parse(self, response):
        detail_urls = response.css('h4 a:not(.greylink)::attr(href)').extract()
        for detail_url in detail_urls:
            detail_url = detail_url.replace("//","")
            detail_url = "https://"+detail_url
            yield Request(url=detail_url, headers=self.headers, callback=self.parse_detail, dont_filter=True)

    # 解析单个汽车的信息
    def parse_detail(self, response):
        name = response.css('h3[class="tab-title"] a::text').extract_first("")
        score = response.css('a.font-score::text').extract_first("")
        comment_nums = response.css('span.count a::text').extract_first("")
        match_re = re.match(r".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        classes = response.css('p[data-gcjid] a::text').extract()
        prices = response.css('div.interval01-list-guidance div::text').extract()
        prices = "".join(prices).replace("\r\n", "").split()
        # {'年款':'价格'}
        groups = dict(zip(classes, prices))
        comment_url = response.css("span.count a::attr(href)").extract_first("")
        if comment_url:
            comment_url = comment_url.replace("//", "")
            comment_url = "https://"+comment_url
            yield Request(url=comment_url, callback=self.parse_comment,
                      headers={'user-agnet': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) ' 'AppleWebKit/537.36 (KHTML, like Gecko) '  'Chrome/61.0.3163.100 Safari/537.36'},
                      dont_filter=True,
                      meta={
                       "name" : name,
                        "score" : score,
                          "comment_nums" : comment_nums,
                          "groups" : groups,
                          "url" : response.url
                      })
        else:
            car_item = CarspiderItem()
            car_item['name'] = name
            car_item['groups'] = groups
            car_item['score'] = score
            car_item['url'] = response.url
            car_item['comment_nums'] = comment_nums
            car_item['comments'] = ""
            yield car_item

    def parse_comment(self, response):
        car_item = CarspiderItem()
        comments = response.css('div.text-con div::text').extract()
        comments = "".join(comments).replace("\r\n","").split()

        car_item['name'] = response.meta['name']
        car_item['groups'] = response.meta['groups']
        car_item['score'] = response.meta['score']
        car_item['url'] = response.meta['url']
        car_item['comment_nums'] = response.meta['comment_nums']
        car_item['comments'] = comments
        yield car_item




