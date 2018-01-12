#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yaro

# 内置库
import json
import random
from urllib.parse import urlencode

# 第三方库
import requests
from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError
import pymongo

# 项目配置
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

base_url = 'http://weixin.sogou.com/weixin?'
headers = {
    'Cookie': 'ABTEST=8|1515253233|v1; IPLOC=CN5000; SUID=FA450A1B771A910A000000005A50EDF1; SUID=FA450A1B2613910A000000005A50EDF1; usid=D5Trs73N2FuTuinN; SUV=00DC5D8E1B0A45FA5A50EDF1F938B697; wuid=AAF9aL+CHQAAAAqROl6zdAMAkwA=; clientId=1F39142291F26B1534FA1F4790326AA4; LSTMV=244%2C320; LCLKINT=8700; weixinIndexVisited=1; JSESSIONID=aaarZCZ9IBAf0hawLCadw; ppinf=5|1515320351|1516529951|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo0NTolRTglQjYlODUlRTclQkElQTclRTUlQjAlOEYlRTQlQjglOEQlRTclODIlQjl8Y3J0OjEwOjE1MTUzMjAzNTF8cmVmbmljazo0NTolRTglQjYlODUlRTclQkElQTclRTUlQjAlOEYlRTQlQjglOEQlRTclODIlQjl8dXNlcmlkOjQ0Om85dDJsdUFZZ1RqQURiaTlZZ2drUWZaSGpHSFVAd2VpeGluLnNvaHUuY29tfA; pprdig=WzCndfLMR68j7og5yxZqFY_EUxyM2I1CmMNB5Usyulgjc07NnAGZcnIsqhum2L14FTcKH3IgLACtGIWhvGe1DqE7kxgH1SkP51sv2S92nSTodrQzQEtQ6fP_Yb3ruvEUOrflKL8f-ttssTgIiZeXlNsVecjw5AFykiMjMA_RJqI; sgid=06-30696483-AVpR9B8KAwH4v6PvzSFSNSM; PHPSESSID=9e98n1eojvv86fgv5d1cg3jeh6; SUIR=48F4B8AAB2B7D3ACD30C9414B207AC5C; SNUID=21B361706B690E417315B0D86C2B4785; wapsogou_qq_nickname=%E8%B6%85%E7%BA%A7%E5%B0%8F%E4%B8%8D%E7%82%B9; w_userid=zL9Mk+JNot9/teBZpehBmt9/xOFpx9Bgy81gtsZPxu9QyuQG0OVA1qR7zOM=_-1675317630; wapsogou_qq_headimg=http%3A%2F%2Fwx.qlogo.cn%2Fmmopen%2Fvi_32%2FCy2Q6LjNamP10KahF1a33Eicnrd6rwiaN2CmSfmUbAcSXT5dXpObuUqJNTvkKnbsx1rRsLeOfFTNw3uLRYialNS4A%2F96; ppmdig=151537466400000060b8781bc9c2c2f70bf8812554da5d69; sct=5',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

proxies = None


def get_proxy():
    """
    从代理池中随机取出一个代理
    :return: requests.get方法的proxies参数
    """
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            proxies_str = response.text
        else:
            print('代理池出错')
            return None
    except ConnectionError:
        print('代理池出错')
        return None
    proxies_list = json.loads(proxies_str)  # 将字符串转换成list
    index = random.randrange(0, len(proxies_list))  # 随机一个index索引值
    proxies_random = {
        'http': 'http://{ip}:{port}'.format(ip=proxies_list[index][0], port=proxies_list[index][1])
    }  # 获取requests.get方法的proxies参数
    return proxies_random


def get_index(keyword, page, count=1):
    """
    请求搜索结果index页面，返回302状态码时，调用代理
    :param keyword: 搜索关键词
    :param page: 搜索结果第几页
    :param count: 某代理ip出错的次数
    :return: index页面的html源码
    """
    query_parameter = {
        'type': 2,
        'query': keyword,
        'page': page
    }
    url = base_url + urlencode(query_parameter)  # 构建index的url
    print('爬取中...', url)
    print('当前请求次数', count)
    global proxies
    if count >= MAX_COUNT:
        print('请求太多次')
        return None
    try:
        if proxies:  # 默认None， 如果有代理，使用代理
            r = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:  # 如果代理为None，不使用代理
            r = requests.get(url, allow_redirects=False, headers=headers)
        if r.status_code == 200:
            index_html = r.text
            return index_html
        if r.status_code == 302:
            proxies = get_proxy()  # 修改全局变量proxies
            if proxies:  # 如果proxies不为None，重新迭代执行get_index()函数
                print('遇到反爬虫302跳转，正在使用代理: ', proxies)
                return get_index(keyword, page)
            else:
                print('获取代理出错')
                return None
    except ConnectionError as e:
        print('出现错误', e.args)
        proxies = get_proxy()
        count += 1
        return get_index(keyword, page, count)


def parse_index(index_html):
    """
    解析搜索结果index页面
    :param index_html:index页面的html源码
    :return: 各文章页面的url
    """
    d = pq(index_html)
    items = d('.news-box .news-list li h3 a').items()
    for item in items:
        yield item.attr('href')


def get_article(article_url):
    """
    请求文章页面，获得html源码
    :param article_url: 文章url
    :return: 文章的html源码
    """
    try:
        r = requests.get(article_url)
        if r.status_code == 200:
            article_html = r.text
            return article_html
        return None
    except ConnectionError:
        return None


def parse_article(article_html):
    """
    解析文章页面，获得目标数据
    :param article_html: 文章html源码
    :return: 文章的数据
    """
    d = pq(article_html)
    title = d('#activity-name').text()
    content = d('.rich_media_content ').text()
    data = d('#post-date').text()
    nickname = d('#post-user').text()
    wechat = d('#js_profile_qrcode > div > p:nth-child(3) > span').text()
    return {
        'title': title,
        'content': content,
        'data': data,
        'nickname': nickname,
        'wechat': wechat
    }


def save_to_mongo(article_data):
    """
    保存文章数据到MongoDB
    :param article_data:
    :return:
    """
    try:
        if db['articles'].update({'title': article_data['title']}, {'$set': article_data}, True):  # 更新
            print('Saved to MongoDB', article_data['title'])
        else:
            print('Saved to MongoDB Failed', article_data['title'])
    except Exception:
        return None


def main():
    for page in range(1, 101):  # 获取1-100页
        index_html = get_index(KEYWORD, page)  # 获取index页面html源码
        if index_html:
            article_urls = parse_index(index_html)  # 解析index页面html源码，获得文章url
            for article_url in article_urls:
                article_html = get_article(article_url)  # 获得文章的html源码
                if article_html:
                    article_data = parse_article(article_html)  # 获取文章的数据
                    print(article_data)
                    if article_data:
                        save_to_mongo(article_data)  # 保存数据到MongoDB


if __name__ == '__main__':
    main()
