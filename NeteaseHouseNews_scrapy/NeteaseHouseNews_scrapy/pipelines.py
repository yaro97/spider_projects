# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo


class JsonPipeline(object):
    def __init__(self):
        self.f = open('netease.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()


class MongoPipeline(object):
    collection_name = 'netease_news_scrapy'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # 此class方法实现访问settings，return必须为Pipeline类
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        # 初始化MongoDB
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # 关闭爬虫前，关闭数据库
        self.client.close()

    def process_item(self, item, spider):
        # 需要把item转换为dict
        # 请尽量使用insert_one and inset_many， 尽量少用insert
        self.db[self.collection_name].insert_one(dict(item))
