# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentHrScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 职位名
    positionName = scrapy.Field()
    # 职位详情链接
    positionLink = scrapy.Field()
    # 职位类别
    positionType = scrapy.Field()
    # 职位数量
    peopleNumber = scrapy.Field()
    # 工作地点
    workLocation = scrapy.Field()
    # 发布日期
    publishTime = scrapy.Field()
