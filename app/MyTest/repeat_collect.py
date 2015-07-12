# -*- coding: utf-8 -*-

from uiautomator import Device
import os
import re
import time
import subprocess

# 获取设备中的所有包名
def appName():
	cmd = 'adb -s ' + series + ' shell pm list packages'
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
	                    stderr=subprocess.STDOUT, shell = True)
	#p = check_output(cmd, shell = True)
	p.wait()
	output=p.stdout.readlines()
	output=set(x.split(':')[1].strip() for x in output)
	return output

def touch(node_bounds):
    node_bounds = node_bounds[1: len(node_bounds) - 1]
    node_bounds = node_bounds.split('][')
    node_bounds[0] = node_bounds[0].split(',')
    node_bounds[0] = map(float, node_bounds[0])
    node_bounds[1] = node_bounds[1].split(',')
    node_bounds[1] = map(float, node_bounds[1])
    x = 0.5 * (node_bounds[1][0] - node_bounds[0][0]) + node_bounds[0][0]
    y = 0.5 * (node_bounds[1][1] - node_bounds[0][1]) + node_bounds[0][1]
    dev.click(x, y)

def ui_interact():
    for i in range(8):
        xml = dev.dump()
        scroll = re.findall(r'.*?scrollable=\"true\".*?', xml)
        all_text = re.findall(r'.*?text=.*?', xml)
        none_text = re.findall(r'.*?text=\"\".*?', xml)
        if len(scroll) == 1 and (len(all_text) - len(none_text)) <= 2:
            print 'single scroll '
            # scroll = re.search(r'.*?scrollable=\"true\".*?bounds=\"(.*?)\"', xml)
            dev.swipe(476, 473, 115, 473, 10) # for 480 * 800
            #dev.swipe(600, 0, 0, 0)
        else:
            break
    time.sleep(10)
    xml = dev.dump()
    clickable = re.findall(r'.*?clickable=\"true\".*?bounds=\"(.*?)\"', xml)
    if len(clickable) == 1:
        node_bounds = clickable[0]
        touch(node_bounds)
        print 'single click'
    # if detect update info, if 取消， 否
    option_cancle = [u'否', u'取消', u'不升级', u'稍后再说', u'稍后', u'稍后更新', u'不更新', u'Not now']
    for i in range(5):
        time.sleep(2)
        xml = dev.dump()
        clickable = re.findall(r'.*?clickable=\"true\".*?bounds=\"(.*?)\"', xml)
        if len(clickable) <= 3:
            print 'found two clickables'
            # re.findall(r'.*?text=\"(.*?)\".*?[^(text=)].*?clickable=\"true\".*?', xml)
            nodelist = xml.split('><')
            for line in nodelist:
                if re.search('.*?clickable=\"t.*?', line):
                    texts = re.findall(r'text="(.*?)"', line)
                    print texts
                    for text in texts:
                        if text in option_cancle:
                            clickable = re.findall(r'bounds=\"(.*?)\"', line)[0]
                            node_bounds = clickable
                            touch(node_bounds)
                            print 'click cancle'
                        else:
                            break

    time.sleep(15)

def visit(arg, dirname, files):
    global self_row
    for filename in files:
        if re.search('apk', filename) and not re.search('log', filename) :
            os.system('adb devices')
            before = appName()
            package = filename
            os.system('adb -s ' + series + ' install ' + dirname + '/' + package)
            after = appName()
            # 集合运算，取差集
            applist = after - before
            if  len(applist) != 1:
                print filename
                print applist
                print 'error! not a single app selected!'
                continue
            for pkg in applist:
                os.popen('adb -s ' + series + ' shell monkey -p ' + pkg + ' --ignore-crashes 1')
                ui_interact()
                cmd1= 'adb -s ' + series + ' shell /system/bin/screencap -p /sdcard/screenshot.png'
                os.system(cmd1)
                cmd1 = 'adb -s ' + series + ' pull /sdcard/screenshot.png ./' + package + current_time + '.png'
                os.system(cmd1)
                dev.dump('first-page.xml')
                os.system('adb -s ' + series + ' uninstall ' + pkg)
                print filename

ISOTIMEFORMAT='%m%d-%H-%M-%S'
current_time = time.strftime(ISOTIMEFORMAT, time.localtime())

series = '0123456789ABCDEF'
# series = '014E233C1300800B'
dev = Device(series)
dir = '/home/hao/Documents/Loc/Operational/loc.map.baidu.com/com.ican.appointcoursesystem/'
os.path.walk(dir, visit, None)
