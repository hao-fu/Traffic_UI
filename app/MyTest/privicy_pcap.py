#!/usr/bin/env python2
#-*-encoding:utf-8-*-
__author__ = 'Hao Fu'

import os
import time
import difflib
import subprocess
import re
from datetime import datetime
from uiautomator import Device#device as dev
import logging

# get app name
def appName():
    cmd = 'adb -s ' + series + ' shell pm list packages'
    app_process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, shell = True)
    #p = check_output(cmd, shell = True)
    app_process.wait()
    output = app_process.stdout.readlines()
    output = set(x.split(':')[1].strip() for x in output)
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
        time.sleep(1)
        xml = dev.dump()
        scroll = re.findall(r'.*?scrollable=\"true\".*?', xml)
        all_text = re.findall(r'.*?text=.*?', xml)
        none_text = re.findall(r'.*?text=\"\".*?', xml)
        if len(scroll) == 1 and (len(all_text) - len(none_text)) == 0:
            # scroll = re.search(r'.*?scrollable=\"true\".*?bounds=\"(.*?)\"', xml)
            #dev.swipe(400, 0, 0, 0) # for 480 * 800
            dev.swipe(576, 473, 115, 473, 10)
        else:
            break
    time.sleep(10)
    xml = dev.dump()
    clickable = re.findall(r'.*?clickable=\"true\".*?bounds=\"(.*?)\"', xml)
    if len(clickable) == 1:
        node_bounds = clickable[0]
        touch(node_bounds)
        print 'click single'
    # if detect update info, if 取消， 否
    option_cancle = [u'否', u'取消', u'不升级', u'稍后再说', u'稍后', u'稍后更新', u'不更新']
    for i in range(5):
        time.sleep(2)
        xml = dev.dump()
        clickable = re.findall(r'.*?clickable=\"true\".*?bounds=\"(.*?)\"', xml)
        if len(clickable) == 2:
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

#series = 'emulator-5554'
series = '014E233C1300800B'
#series = '01b7006e13dd12a1'
#os.popen('rm -r -f data')
os.popen('mkdir data')
#package = 'com.google.android.deskclock'
#package = 'com.android.settings'
ISOTIMEFORMAT = '%m%d-%H-%M-%S'
filelist = os.listdir('.') # list files at current dir
# set threashold large to check behaviors underware
logger = logging.getLogger('UiDroid-Console')
logger.setLevel(logging.DEBUG)

consolehandler = logging.StreamHandler()
consolehandler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
consolehandler.setFormatter(formatter)


logger.addHandler(consolehandler)


#package_pattern = re.compile(r'.*apk')
register_pattern = re.compile(r'.*(Regis|REGIS|Sign|SIGN).*')
fline_pattern = re.compile(r'(.*?).json')
dev = Device(series)
for fline in filelist:
    if fline_pattern.match(fline):
            continue
    #fmatch = package_pattern.match(fline)
    #if not fmatch:
    #   continue
    os.popen('adb devices')
    before = appName()
    os.popen('adb -s ' + series +' install ' + fline)
    after = appName()
    applist = after - before
    if len(applist) != 1:
        logger.info(fline)
        logger.info(applist)
        logger.info('error! not a single app selected!')
        os.system('rm ' + fline)
        # break
        continue
    for package in applist:
        os.popen('adb -s ' + series + ' shell am start -n fu.hao.uidroid/.TaintDroidNotifyController')
        current_time = time.strftime(ISOTIMEFORMAT, time.localtime())
        os.popen('adb -s ' + series + ' shell "su 0 date -s `date +%Y%m%d.%H%M%S`"')
        os.popen('adb -s ' + series + ' shell monkey -p com.lexa.fakegps --ignore-crashes 1')
        dev.info 
        dev.screen.on()
        #dev(text='Set location').click()
        dev.click(300, 150)
        dev.press.back()
        os.popen('adb kill-server')
        os.popen('adb start-server')
        cmd = 'adb -s ' + series + ' shell "nohup /data/local/tcpdump -w /sdcard/' + package + current_time + '.pcap"'
        #os.system(cmd)
        subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, shell=True)
        logger.info('tcpdump begins')
        os.popen('adb -s ' + series + ' logcat -c')
        logger.info('clear logcat')
        dir_data = 'data/' + package + '/'
        os.popen('mkdir ' + dir_data)
        #os.popen('adb -s ' + series + ' shell "logcat -v threadtime | grep --line-buffered UiDroid_Taint > /sdcard/' + package + current_time +'.log " &')
        cmd = 'adb -s ' + series + ' shell "nohup logcat -v threadtime -s "UiDroid_Taint" > /sdcard/' + fline + current_time +'.log"'
        #os.system(cmd)
        subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, shell=True)
        logger.info('logcat start')
        #time.sleep(20)
        os.popen('adb -s ' + series + ' shell monkey -p ' + package + ' --ignore-crashes 1')
        
        #package_list = os.popen('adb -s ' + series + ' shell cat /data/system/packages.list')
        #logger.info(package_list.readlines())
        #ps_list = os.popen('adb -s ' + series + ' shell ps')
        #logger.info(ps_list.readlines())

        
        filehandler = logging.FileHandler(dir_data + '/UiDroid-Console.log')
        filehandler.setLevel(logging.DEBUG)
        logger.addHandler(filehandler)
        filehandler.setFormatter(formatter)

        
        #time.sleep(30)
        ui_interact()
        # dev.screenshot(dir_data + current_time + ".png")
        os.system('adb -s ' + series + ' shell /system/bin/screencap -p /sdcard/screenshot.png')
        os.system('adb -s ' + series + ' pull /sdcard/screenshot.png ' + dir_data)
        dev.dump(dir_data + current_time + "hierarchy.xml")
        logger.info('screen shot at ' + current_time)

        
        dev.screen.on()
        dev.press.home()
        time.sleep(20)
        #package_list = os.popen('adb -s ' + series + ' shell cat /data/system/packages.list')
        #logger.info(package_list.readlines())
        #ps_list = os.popen('adb -s ' + series + ' shell ps')
        #logger.info(ps_list.readlines())
        os.popen('adb -s ' + series + ' shell am force-stop ' + package)
        os.popen('adb -s ' + series + ' uninstall ' + package)
        logger.info('uninstall')
        os.popen('adb -s ' + series + ' logcat -c')
        kill_status = os.popen('adb -s ' + series + ' shell ps | grep logcat | awk \'{print $2}\' | xargs adb -s ' + series + ' shell kill')
        logger.info(kill_status.readlines())
        kill_status = os.popen('adb -s ' + series + ' shell ps | grep tcpdump | awk \'{print $2}\' | xargs adb -s ' + series + ' shell kill')
        logger.info(kill_status.readlines())
        kill_status = os.popen('adb -s ' + series + ' shell am force-stop fu.hao.uidroid')
        logger.info(kill_status.readlines())
        pull_status = os.popen('adb -s ' + series + ' pull /sdcard/' + package + current_time + '.pcap ' + dir_data)
        logger.info(pull_status.readlines())
        os.popen('adb -s ' + series + ' shell rm /sdcard/' + package + current_time + '.pcap')
        pull_status = os.popen('adb -s ' + series + ' pull /sdcard/' + fline + current_time + '.log ' + dir_data)
        logger.info(pull_status.readlines())
        os.popen('adb -s ' + series + ' shell rm /sdcard/' + fline + current_time + '.log')
        os.system('mv ' + fline + ' ' + dir_data)
