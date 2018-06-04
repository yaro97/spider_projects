#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yaro
# The Economist（经济学人）高频词汇（全），
# 抓取高频词汇（3162个）网页：https://www.shanbay.com/wordbook/104617/
# 抓取经济学人（2W）网页：https://www.shanbay.com/wordbook/168862/




import requests
from pyquery import PyQuery as pq


def get_list(list_url):
    """
    获取开始列表页的html
    :param list_url:
    :return:
    """
    list_html = requests.get(list_url)
    return list_html.text


def parse_list(list_html):
    """
    解析出各个详情页的url
    :param list_html:
    :return:
    """
    doc = pq(list_html)
    detail_urls = doc('.wordbook-wordlist-name a').items()
    for detail_url in detail_urls:
        yield detail_url.attr('href')


def get_detail(detail_url):
    """
    获得详情页的html
    :param detail_url:
    :return:
    """
    detail_html = requests.get(detail_url)
    return detail_html.text


def parse_detail(detail_html):
    """
    解析出某个详情页中的所有的单词
    :param detail_html:
    :return:
    """
    doc = pq(detail_html)
    words = doc('.row strong').items()
    for word in words:
        yield word.text()


def save_to_file(word):
    with open('word.txt', 'a') as f:
        f.write(word)


def main():
    list_url = 'https://www.shanbay.com/wordbook/168862/'
    list_html = get_list(list_url)
    for detail_url in parse_list(list_html):
        base_detail_url = 'https://www.shanbay.com' + detail_url + '?page={}'
        detail_urls = [base_detail_url.format(i) for i in range(1, 11)]
        for url in detail_urls:
            detail_html = get_detail(url)
            words = parse_detail(detail_html)
            for word in words:
                print(word)
                save_to_file(word + '\n')


if __name__ == '__main__':
    main()
