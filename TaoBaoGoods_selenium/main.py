#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yaro

# 内置库
import re

# 第三方库
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import pymongo

# 项目文件
from config import *

# 设置MongoDB
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# 设置浏览器
driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
driver.set_window_size(1400, 900)

wait_until = WebDriverWait(driver, 10).until


def search(taobao_url, keyword):
    """
    根据关键词请求页面
    :param taobao_url:
    :param keyword: 搜索啥?
    :return: 搜索结果的总页数
    """
    print("正在搜索...")
    try:
        driver.get(taobao_url)
        search_input = wait_until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))  # 等待"搜索框"加载完成,并赋值
        search_submit = wait_until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button")))  # 等待"搜索按钮"加载完成,并赋值
        search_input.send_keys(keyword)  # 输入"keyword"到"搜索框"
        search_submit.click()  # 搜索
        total_page_num_text = wait_until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total")))  # 等待"共xxx页"加载完成,并赋值
        total_page_num = int(re.compile('(\d+)').search(total_page_num_text.text).group(1))  # 获取"共xxx页"中的"xxx"(数字)
        return total_page_num
    except TimeoutException:
        return search(taobao_url, keyword)


def next_page(page_num):
    """
    通过输入的指定页数,翻页
    :param page_num: 搜索页面底部:"到第xx页"
    :return:None
    """
    print("正在翻页...")
    try:
        page_num_input = wait_until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        page_num_submit = wait_until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
        page_num_input.clear()
        page_num_input.send_keys(page_num)
        page_num_submit.click()
        wait_until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"),
            str(page_num)))  # 判断是否是page_num页
    except TimeoutException:
        next_page(page_num)


def get_products():
    """
    解析当前页面,得到各个产品的信息(生成器)
    :return: 当前页面各产品的信息
    """
    wait_until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .items .item")))  # 等待当前页产品信息加载结束
    d = pq(driver.page_source)  # 把当前页html源码转化为PyQuery对象
    products = d.find("#mainsrp-itemlist .items .item").items()  # 解析当前页所有产品(列表)
    for product in products:
        yield {
            "image": product.find(".pic .img").attr("src"),
            "price": product.find(".price").text(),
            "deal": product.find(".deal-cnt").text()[:-3],
            "title": product.find(".title").text(),
            "shop": product.find(".shop").text(),
            "location": product.find(".location").text()
        }


def save_to_mongo(product):
    """
    保存到MongoDB
    :param product:某个产品的信息
    :return: None
    """
    try:
        if db[MONGO_TABLE].insert(product):
            print("保存到MongoDB成功", product)
    except Exception:
        print("保存到MongoDB失败", product)


def main():
    try:
        # 执行search函数,并返回搜索结果总页数(int)
        total_page_num = search(TAOBAO_URL, KEYWORD)

        # 保存首页每一个product信息到数据库
        for product in get_products():
            save_to_mongo(product)

        # 循环第2页之后的页面
        for page_num in range(2, total_page_num + 1):
            next_page(page_num)
            for product in get_products():
                save_to_mongo(product)

    # except Exception:
    #     print("貌似哪儿出错了!!")
    finally:
        driver.close()


if __name__ == '__main__':
    main()
