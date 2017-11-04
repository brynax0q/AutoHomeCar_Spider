# -*- coding: utf-8 -*-
import codecs
import json
import csv
from scrapy.exporters import CsvItemExporter
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



class CarspiderPipeline(object):
    def process_item(self, item, spider):
        pass
        return item


class JasonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('cars.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class htmlPipeline(object):
    def __int__(self):
        self.file = codecs.open('cars.html', 'w', encoding='utf-8')  # 以写方式打开 output.html 文件
        self.file.write("<html>")
        self.file.write("<bode>")
        self.file.write("<table>")  # 表格标签
    def process_item(self, item, spider):
        # print(item)
        self.file.write("<tr>")  # 行开始标签
        self.file.write("<td>%s</td>" % item['name'])
        self.file.write("<td>%s</td>" % item['groups'])  # 以utf-8编码输出
        self.file.write("<td>%s</td>" % item['score'])
        self.file.write("<td>%s</td>" % item['url'])
        self.file.write("<td>%s</td>" % item['comment_nums'])
        self.file.write("<td>%s</td>" % item['comment'])
        self.file.write("</tr>")
        return item

    def spider_closd(self):
        self.file.write("</table>")
        self.file.write("</bode>")
        self.file.write("</html>")
        self.file.close()





