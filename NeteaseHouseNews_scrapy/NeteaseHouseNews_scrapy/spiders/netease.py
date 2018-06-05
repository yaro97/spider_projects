# -*- coding: utf-8 -*-
import scrapy
from NeteaseHouseNews_scrapy.items import NeteaseScrapyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class NeteaseSpider(CrawlSpider):
    name = "netease"
    allowed_domains = ["163.com"]
    start_urls = ['http://money.163.com/special/002534NU/house2010.html']
    # 定义rules，follow设置为True，注意callback参数为字符串
    rules = [
        Rule(LinkExtractor(allow='special/002534NU/house2010.*\.html'), callback='parse_list', follow=True)
    ]

    def parse_list(self, response):
        # 不要使用默认的parse函数
        article_urls = response.css('.list_item h2 a::attr(href)').extract()
        # print(article_urls)
        for article_url in article_urls:
            yield scrapy.Request(article_url, self.parse_detail)

    def parse_detail(self, response):
        item = NeteaseScrapyItem()
        item['title'] = response.css('h1::text').extract_first()
        item['time'] = response.css('.post_time_source::text').extract_first().strip()[:19]
        item['source'] = response.css('#ne_article_source::text').extract_first()
        item['editor'] = response.css('.ep-editor::text').extract_first()[5:]
        item['content'] = response.css('.post_text p::text').extract()
        # print(item['title'])
        yield item
