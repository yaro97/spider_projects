# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NeteaseScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()
    editor = scrapy.Field()
    content = scrapy.Field()
    # pass
