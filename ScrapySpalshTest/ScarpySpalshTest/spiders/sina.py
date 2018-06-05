# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class SinaSpider(scrapy.Spider):
    name = "sina"
    allowed_domains = ["sina.com.cn"]
    start_urls = ['http://blog.sina.com.cn/s/blog_4d9312c60102zckq.html?tj=fina']

    def start_requests(self):
        args = {
            'wait': 0.5
        }
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse, args=args)

    def parse(self, response):
        author = response.css('.introduct p a').extract()
        # author = response.css('title').extract()
        print('作者是： ', author)
