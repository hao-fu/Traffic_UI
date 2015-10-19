# -*- coding: utf-8 -*-
__author__ = 'hao'

import os
import re

def write_pcap_txt(dirname, pcap, flag):
    if flag:
        result = os.popen('parse_pcap  -vv ' + dirname + '/' + pcap + ' > ' + dirname + '/' + pcap.split('.pcap')[0] + '.txt')
        #print result
    return dirname + '/' + pcap.split('.pcap')[0] + '.txt'

def visit(arg, dirname, files):
    appname = dirname.split('/')
    appname = appname[len(appname) - 1]
    if appname in already_apps:
        return
    for filename in files:
        if re.search('.pcap', filename):
            pcap = filename
            txt = write_pcap_txt(dirname, pcap, False)
            try:
                txt = open(txt, 'r')
            except IOError as e:
                #print 'ERROR: ' + e.message
                txt = write_pcap_txt(dirname, pcap, True)
                txt = open(txt, 'r')
                return
            lines = txt.readlines()
            appname_flag = True
            unseen = []
            for line in lines:
                for keyword in keywords:
                    flag = False
                    if re.search(keyword, line):
                        try:
                            for anti_keyword in anti_keywords[keyword]:
                                if re.search(anti_keyword, line):
                                    #print 'ANTI'
                                    flag = True
                                    break
                        except:
                            if appname_flag:
                                print appname + '++++++++++++++++++++++++++++++++++++++++'
                                log.write(appname + '++++++++++++++++++++++++++++++++++++\n')


                        if not flag:
                            if appname_flag:
                                print appname + '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
                                log.write(appname + '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
                                appname_flag = False
                                os.popen('cp -r ' + dirname + ' ' + outdir)

                            #print keyword + ': ' + line
                            if line not in unseen:
                                print keyword + ': ' + line
                                log.write(keyword + ': ' + line + '\n')
                                unseen.append(line)
                                break

def already_app_list(arg, dirname, files):
    appname = dirname.split('/')
    appname = appname[len(appname) - 1]
    if appname not in already_apps:
        already_apps.append(appname)

# mark loc related flow from pcap based on keywords
keywords = ['-121\.7', '38\.5',
            '-1217',
            'loc.map', 'Davis','davis','gps', 'GPS']

anti_keywords = {
                 'gps': ['gpsx', 'kegps'],
                 'GPS': ['gpsx', 'kegps']}

already_dir = '/home/hao/Documents/Ground/'
already_apps = []
os.path.walk(already_dir, already_app_list, None)
print already_apps

dir = '/media/hao/Hitachi/BaiduApks/software/504/4/LOC/data/'
outdir = '/home/hao/Documents/Ground/missed/4/'
log = open('taint_missed41.log', 'w')
os.path.walk(dir, visit, None)
log.close()

