# -*- coding: utf-8 -*-
import scrapy
import json
from DouyuImage_scrapy.items import DouyuimageScrapyItem


class DouyuSpider(scrapy.Spider):
    name = "douyu"
    allowed_domains = ["douyucdn.cn"]
    base_url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset={}'
    offset = 0
    start_urls = [base_url.format(offset)]

    def parse(self, response):
        data_list = json.loads(response.text)
        # if not len(data_list):
        if self.offset > 1:
            return

        item = DouyuimageScrapyItem()
        for data in data_list['data']:
            item['nickname'] = data['nickname']
            item['image_urls'] = data['vertical_src']
            yield item

        # 循环抓取所有Ajax页面
        self.offset += 20
        yield scrapy.Request(self.base_url.format(self.offset), callback=self.parse)
