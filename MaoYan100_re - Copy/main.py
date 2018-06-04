#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
# from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import requests
from requests.exceptions import RequestException


def get_index_page(index_url):
    """
    获取index页html源码
    :param index_url: 列表页的URL
    :return: 列表页html源码
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      + 'Chrome/63.0.3239.84 Safari/537.36'}
    try:
        r = requests.get(index_url, headers=headers)
        if r.status_code == 200:
            return r.text
        return None
    except RequestException:
        return None


def parse_index_page(index_html):
    """
    解析index_html,获得目标内容
    :param index_html:
    :return: 各电影的信息(Generator)
    """
    prog = re.compile('<dd>.*?href="(.*?)".*?title="(.*?)".*?'
                      + 'class="star">(.*?)</p>.*?time">(.*?)</p>.*?'
                      + 'integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = prog.findall(index_html)
    for item in items:
        yield {
            'url': 'http://maoyan.com' + item[0],
            'film_name': item[1],
            'actors': item[2].strip()[3:],
            'release_time': item[3][5:],
            'star': item[4] + item[5]
        }


def save_to_file(item_byte):
    """
    保存到film_100_res.txt
    :param item_byte:
    :return:
    """
    lock = multiprocessing.Lock()

    with open('film_100_res.txt', 'a', encoding='utf-8') as f:
        with lock:
            f.write(item_byte + '\n')


def one_loop(index_url):
    """
    抓取第1页电影信息
    :param index_url:
    :return:
    """
    index_html = get_index_page(index_url)
    items = parse_index_page(index_html)
    for item in items:
        item_byte = json.dumps(item, ensure_ascii=False)
        print(item_byte)
        save_to_file(item_byte)


def main():
    """
    抓取全部10页的电影信息
    :return:
    """
    prefix_url = 'http://maoyan.com/board/4?offset='
    index_urls = [prefix_url + str(j * 10) for j in range(10)]  # 构造index_urls列表,供多进程map函数调用
    with multiprocessing.Pool() as pool:
        pool.map(one_loop, index_urls)

    # for index_url in index_urls:  # 单线程
    #     one_loop(index_url)
    # with ThreadPoolExecutor() as executor:  # 多线程
    #     executor.map(one_loop, index_urls)


if __name__ == '__main__':
    main()
return None
