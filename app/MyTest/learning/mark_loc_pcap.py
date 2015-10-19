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
            '-1217','385',
            'lng', 'longi', 'map', 'Davis', 'weather', 'lat', 'loc',
            'area', 'ditu', 'address'
            'geo', 'Location', 'davis', 'Weather', 'Address', 'Longitude',
            'Latitude', 'Map ', 'Geo', u'地理', u'位置', u'未知', 'gps', 'GPS'
            u'天气', u'风', u'雾', u'雨', 'rain', 'sunny', 'coord']
anti_keywords = {'map': '=map', 'lat': ['plat', 'late', 'elat', 'lato', 'Plat'],
                 'area': 'textarea',
                 'loc': ['velocity', 'bloc', 'cloc', 'Veloc', 'ion.href', 'nt.loc',
                         'local', 'loctp', 'ow.loca', 'iloc', 'Bloc', 'lock', 'location: '],
                 'lon': ['f-long', 'longTa', 'clon', 'lone'],
                 'Address': ['rAddress', 'eAddress'],
                 'gps': ['gpsx']}

already_dir = '/home/hao/Documents/Ground/'
already_apps = []
os.path.walk(already_dir, already_app_list, None)
print already_apps

dir = '/media/hao/Hitachi/BaiduApks/software/504/3/LOC/data/'
log = open('taint_missed31.log', 'w')
os.path.walk(dir, visit, None)
log.close()

