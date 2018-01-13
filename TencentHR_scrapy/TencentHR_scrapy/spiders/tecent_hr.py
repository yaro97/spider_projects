# -*- coding: utf-8 -*-
import scrapy
from TencentHR_scrapy.items import TencentHrScrapyItem


class TecentHrSpider(scrapy.Spider):
    name = "tencent_hr"
    allowed_domains = ["tencent.com"]
    base_url = 'http://hr.tencent.com/position.php?&start='
    offset = 0
    start_urls = [base_url + str(offset)]  # 构建第一页

    def parse(self, response):
        positions = response.css('#position .even,.odd')  # 提取单页所有职位信息
        for position in positions:
            item = TencentHrScrapyItem()  # 构建item对象，用来保存数据
            # 提取每个职位的具体信息
            item['positionName'] = position.css('td:nth-child(1) a::text').extract()[0]
            item['positionLink'] = 'http://hr.tencent.com/' + position.css('td:nth-child(1) a::attr(href)').extract()[0]
            if position.css('td:nth-child(2)::text').extract():  # 有的职位type为空，判断下
                item['positionType'] = position.css('td:nth-child(2)::text').extract()[0]
            else:
                item['positionType'] = ''
            item['peopleNumber'] = position.css('td:nth-child(3)::text').extract()[0]
            item['workLocation'] = position.css('td:nth-child(4)::text').extract()[0]
            item['publishTime'] = position.css('td:nth-child(5)::text').extract()[0]
            yield item

        if not response.css('.tablelist .pagenav .noactive#next'):  # 如果不是最后一页（"下一页"不可用）
            self.offset += 10
            url = self.base_url + str(self.offset)
            yield scrapy.Request(url, callback=self.parse)  # 重新调用回调函数parse解析下一页
