# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["sina.com.cn"]
    start_urls = ['https://s.taobao.com/search?spm=a21bo.2017.201856-fline.2.5c2b2bc4OyE2xT&q=%E5%9B%9B%E4%BB%B6%E5%A5%97&refpid=420461_1006&source=tbsy&style=grid&tab=all&pvid=d0f2ec2810bcec0d5a16d5283ce59f67']

    def start_requests(self):
        splash_args = {
            'wait': 0.5,
        }
        for start_url in self.start_urls:
            yield SplashRequest(start_url, callback=self.parse, args=splash_args)

    def parse(self, response):
        deal_cnt = response.css('.deal-cnt::text').extract()
        print('成交量', deal_cnt)
        # price = response.css('.p-price .price::text').extract_first()
        # print('价格', price)
        # tag = response.css('.J-prom .hl_red_bg::text').extract_first()
        # print('标志', tag)


