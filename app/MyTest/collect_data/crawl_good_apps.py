# -*- coding: utf-8 -*-
__author__ = 'hao'

import re
from splinter import Browser

app_list = []
# base_url = 'http://shouji.baidu.com/s?wd=%E5%A4%A9%E6%B0%94&data_type=app&f=header_all%40input?page33#page' # 天气
# base_url = 'http://shouji.baidu.com/s?wd=%E8%BF%90%E5%8A%A8&data_type=app&f=header_all%40input#page' # 运动
base_url = 'http://shouji.baidu.com/s?wd=%E5%9C%B0%E5%9B%BE&data_type=app&f=header_app%40input#page'  # 地图


def get_html(browser):
    html = browser.html
    flag = False
    #print url
    lines = html.split('\n')
    app_pattern = re.compile(r'.*?docid=(.*?)&.*?')
    for line in lines:
        result = app_pattern.match(line)
        if result:
            appid = result.group(1)
            if appid not in app_list:
                app_list.append(appid)
                print appid
                flag = True
    return flag

def getlist(page):
    url = base_url + str(page)
    with Browser('firefox') as browser:
        #print page
        browser.visit(url)
        return get_html(browser)
        #print browser.find_by_css('h1').last.click()
        #while browser.find_by_tag('form').last.click():
            #get_html(browser)

for page in range(1, 42):
        #print page
        counter = 0
        while not getlist(page):
            counter += 1
            if counter > 9:
                break
print app_list

print len(app_list)