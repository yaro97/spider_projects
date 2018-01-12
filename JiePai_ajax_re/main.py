#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard Libraries
import os
import json
from hashlib import md5
from json.decoder import JSONDecodeError
from urllib.parse import urlencode
from concurrent.futures import ProcessPoolExecutor

# Third Party Libraries
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
import pymongo

# Project files
from config import *

client = pymongo.MongoClient(MONGO_URL)  # 声明Mongo客户端
db = client[MONGO_DB]  # 声明Mongo数据库


def get_index_page(index_url):
    """
    获取index页面html源码
    :param index_url:
    :return: index页面html源码
    """
    try:
        r = requests.get(index_url)
        if r.status_code == 200:
            return r.text
        return None
    except RequestException:
        print('请求 index page 错误')
        return None


def parse_index_page(index_html):
    """
    解析index页，获得各detail页的urls(生成器)
    :param index_html:索引页的html源码
    :return: detail_url 各详情页的url地址(生成器)
    """
    try:
        data = json.loads(index_html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass


def get_detail_page(detail_url):
    """
    获取detail_page页html源码
    :param detail_url:详情页的URL
    :return: detail_page页的html源码
    """
    # 之前,获取源码 - 用re提取 - 但转换为Json时出错,暂时用selenium救火;
    driver = webdriver.PhantomJS()
    driver.get(detail_url)
    detail_html = driver.page_source
    return detail_html


def parse_detail_page(detail_url, detail_html):
    """
    解析detail_html，获得目标内容(标题/图片等)
    :param detail_url:
    :param detail_html:
    :return: 我们想要的图片、标题等
    """
    soup = BeautifulSoup(detail_html, 'lxml')
    title = soup.select('title')[0].get_text()
    images_html = soup.select('.image-item a')
    image_urls = [image_html['href'] for image_html in images_html]

    # images_prog = re.compile('gallery: JSON\.parse\("(.*?)"\),', re.S)
    # result = images_prog.search(detail_html).group(1)
    # data = json.loads(res)
    # json.loads() 一直报错"ValueError: 应使用双引号包括name",没有找到原因,暂时搁置!

    return {
        'title': title,
        'url': detail_url,
        'images': image_urls
    }


def save_to_mongo(result):
    """
    把抓取的结果写入MongoDB
    :param result: 目标结果(标题/图片等)
    :return:
    """
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False


def download_image(image_url):
    """
    下载图片到"./images"目录,图片名为md5编码结果
    :param image_url:图片url
    :return:
    """
    print('Downloading Image: ', image_url)
    try:
        r = requests.get(image_url)
        if r.status_code == 200:
            image_content = r.content
            try:
                os.stat('images')  # 查看是否有 images 目录
            except FileNotFoundError:
                os.mkdir('images')  # 新建 images 目录
            image_path = '{}\\images\\{}.{}'.format(os.getcwd(), md5(image_content).hexdigest(), 'jpg')  # for windows
            # image_path = '{}/images/{}.{}'.format(os.getcwd(), md5(image_content), 'jpg')  # fow linux
            if not os.path.exists(image_path):
                with open(image_path, 'wb') as f:
                    f.write(image_content)
        return None
    except RequestException:
        print('请求 Image URL 错误')
        return None


def one_loop(index_url):
    """
    执行所有过程: 根据提供的index_url, 解析数据存入MongoDB, 图片保存到"./images"
    :param index_url:
    :return:
    """
    index_html = get_index_page(index_url)  # 获取索引页html源码
    for detail_url in parse_index_page(index_html):  # 解析索引页源码,获得detail页面的url
        detail_html = get_detail_page(detail_url)  # 获取detail页面的html源码
        if detail_html:
            result = parse_detail_page(detail_url, detail_html)  # 解析detail页面html源码,得到:详情页title/图片url等
            print(result)
            save_to_mongo(result)  # 保存到MongoDB
            for image_url in result['images']:  # 保存各图片到 ./images文件夹下
                download_image(image_url)


def construct_index_url(offset):
    """
    通过 offset 构造 index_url
    :param offset:
    :return:
    """
    request_para = {
        'offset': offset,
        'format': 'json',
        'keyword': KEYWORD,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'from': 'gallery'
    }
    prefix_url = 'https://www.toutiao.com/search_content/?'
    return prefix_url + urlencode(request_para)


def main():
    index_urls = [construct_index_url(i * 20) for i in range(LOOP_START, LOOP_END)]  # 构造 index_urls 列表,供多线程 map 函数调用
    with ProcessPoolExecutor() as pool:  # 多线程
        pool.map(one_loop, index_urls)


if __name__ == '__main__':
    main()
