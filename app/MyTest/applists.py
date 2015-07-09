# -*- coding: utf-8 -*-
__author__ = 'watershed2106'

"""
Spyder Editor
"""
import mechanize
import cookielib
import urllib
import re
import os
from bs4 import BeautifulSoup
from random import randint
from time import sleep

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
# setting
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
base_url = 'http://shouji.baidu.com/software/list'
# User-Agent (this is cheating, ok?)
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'
br.addheaders = [('User-agent',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Chrome/17.0.963.56 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# br.set_debug_http(True)
applist = []
apklist = []
page_id = 8
board_id = raw_input('Input board_id: ')
nav_cate = raw_input('input nav_cate: ')
page_num = 1

def retrive_applist():
    values = {'cid': '50' + str(page_id), 'from': '', 'f': 'list_software_505%40nav_cate%40' + nav_cate, 'page_num': page_num,
              'boardid': 'board_100_0' + str(board_id)}
    data = urllib.urlencode(values)

    geturl = base_url + '?' + data

    # Open the page
    br.open(geturl)
    html = br.response().read()
    print geturl
    # print html

    # pattern = re.compile('<div.*?class="app-box.*?>.*?<a href=(.*?)&form.*?>', re.S)
    app_pattern = re.compile(r'.*?docid=(.*?)&.*?')
    category_pattern = re.compile(r'.*?<li><a.*?class="cur".*?>(.*?)<.*?')
    subcategory_pattern = re.compile(r'.*?</span><a.*?class="cur".*?>(.*?)<.*?')
    apk_pattern = re.compile(r'.*?data_url=(.*?)')
    lines = html.split('\n')
    for line in lines:
        result = app_pattern.match(line)
        result_category = category_pattern.match(line)
        result_subcategory = subcategory_pattern.match(line)
        result_apk = apk_pattern.match(line)
        if result:
            apkid = result.group(1)
            applist.append(apkid)
            print apkid
        elif result_category:
            global category
            category = result_category.group(1)
            os.system('mkdir ' + category)
            print result_category.group(1)
        elif result_subcategory:
            global subcategory
            subcategory = result_subcategory.group(1)
            os.system('mkdir ' + category + '/' + subcategory)
        elif result_apk:
            line = line.split('"')
            apklist.append(line[1])

        # items = re.findall(pattern, html)
        # print len(items)
        # for item in items:
        #   print item[0]

        # soup = BeautifulSoup(html)
        # print soup.div
        # print soup.prettify()

for i in range(1, 20):
    retrive_applist()
    #page_id += 1
    #board_id = int(board_id) + 1
    page_num += 1

print len(applist)
subcategory = None
file = open(category + '/' + subcategory + '/' + category + '-' + subcategory + '.txt', 'w')
for i in range(len(applist)):
    file.write("%s \n" %applist[i])
download = open(category + '/' + subcategory + '/' + 'download.txt', 'w')
for i in apklist:
    download.write("%s \n" %i)

#os.system('wget ')


