# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class TencenthrScrapyPipeline(object):
    def __init__(self):
        # 初始化，可以使用 start_spider
        self.f = open('tencent_hr.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 写入文件
        content = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.f.write(content)
        return item

    def close_spider(self, spider):
        # 关闭爬虫时，关闭关闭文件
        self.f.close()
