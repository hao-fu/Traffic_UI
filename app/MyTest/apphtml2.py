__author__ = 'hao'
# -*- coding: utf-8 -*-
"""
Spyder Editor
"""
import mechanize
import cookielib
import urllib
import socket

# get app info htmls from Baidu

def get_html():
    global timeout_occurred
    values = {'docid': docid}
    data = urllib.urlencode(values)
    geturl = base_url + '?' + data
    while timeout_occurred:
        try:
            # Open the page
            br.open(geturl, timeout=1.5)
            html = br.response().read()
            timeout_occurred = False
        except socket.timeout:
                timeout_occurred = True
        except mechanize.URLError as exc:#mechanize.URLError as exc:
            if isinstance(exc.reason, socket.timeout):
                timeout_occurred = True
        # retry
        #br.open(geturl, timeout=5)
    timeout_occurred = True

    file = open('/media/hao/Hitachi/BaiduApks/html/' + str(docid) + '.html', 'w')
    file.write(html)
    print geturl

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
# setting
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
base_url = 'http://shouji.baidu.com/soft/item'
# User-Agent (this is cheating, ok?)
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'
br.addheaders = [('User-agent',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Chrome/17.0.963.56 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# br.set_debug_http(True)
docid = 7658666 #7400000 #7233942
timeout_occurred = True
for i in range(0, 50000):
    get_html()
    docid += 1