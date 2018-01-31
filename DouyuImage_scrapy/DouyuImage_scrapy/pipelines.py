# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os
from DouyuImage_scrapy.settings import IMAGES_STORE


# class DouyuimageScrapyPipeline(object):
#     def process_item(self, item, spider):
#         return item


class DouyuimageScrapyPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_urls'])

    def item_completed(self, results, item, info):
        # print(results)
        # print('*'*20)
        # 取出results中的图片path
        image_path = [x['path'] for singal, x in results if singal]
        os.rename(IMAGES_STORE + image_path[0], IMAGES_STORE + item['nickname'] + '.jpg')
        return item
