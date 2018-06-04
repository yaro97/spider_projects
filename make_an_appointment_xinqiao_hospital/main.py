#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yaro
# 这年头看病不容易，有些nb的医生号压根拿不到。
# 目标网站：http://61.186.173.202:8099/xqyygh/
# 目标医生：xxx

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()
base_url = "http://61.186.173.202:8099/xqyygh/"


def visit_url(url):
    try:
        driver.get(url)
        quick_reserve = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".main_left .ks_menu li:first-child"))
        )
        quick_reserve.click()
        confirm = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#confirm"))
        )
        confirm.click()

        # ## 晋献春如下：
        department = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#deptCode option:nth-child(21)"))
        )
        department.click()
        doctor = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#doctorNo option:nth-child(3)"))
        )
        doctor.click()
        schedule = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#schedule option:nth-child(3)"))
        )
        schedule.click()
        confirm_reserve = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".kuyy_left>a"))
        )
        confirm_reserve.click()
        name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#name"))
        )
        name.send_keys("黄琴")
        id_code = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#idCode"))
        )
        id_code.send_keys("511126198704090021")
        sex = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#sex option:nth-child(2)"))
        )
        sex.click()
        phone = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#phone"))
        )
        phone.send_keys("18008378618")

        ## 陈勇鹏如下：
        # department = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "#deptCode option:nth-child(21)"))
        # )
        # department.click()
        # doctor = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "#doctorNo option:nth-child(1)"))
        # )
        # doctor.click()
        # schedule = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "#schedule option:nth-child(3)"))
        # )
        # schedule.click()
        # confirm_reserve = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, ".kuyy_left>a"))
        # )
        # confirm_reserve.click()
        # name = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "#name"))
        # )
        # name.send_keys("黄琴")
        # id_code = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "#idCode"))
        # )
        # id_code.send_keys("511126198704090021")
        # sex = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "#sex option:nth-child(2)"))
        # )
        # sex.click()
        # phone = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "#phone"))
        # )
        # phone.send_keys("18008378618")





        # for element in department:
        #     if element == "中医科门诊":
        #         element.click()
        #         break

    # finally:
    #     driver.quit()
    except TimeoutException:
        return visit_url(url)


def main():
    visit_url(base_url)


if __name__ == '__main__':
    main()
