# -*- coding: utf-8 -*-
__author__ = 'hao'

# rm apps already exist in Ground, but not in potential
# then extract pcap flows from them

import os
import re
from scapy.layers.inet import IP, TCP
from scapy.all import *

def write_pcap_txt(dirname, pcap, flag):
    if flag:
        result = os.popen('parse_pcap  -vv ' + dirname + '/' + pcap + ' > ' + dirname + '/' + pcap.split('.pcap')[0] + '.txt')
        #print result
    return dirname + '/' + pcap.split('.pcap')[0] + '.txt'

def visit(arg, dirname, files):
    appname = dirname.split('/')
    appname = appname[len(appname) - 1]
    if appname in already_apps:
        os.popen('rm -rf ' + dirname)
        return
    for filename in files:
        if re.search('.pcap', filename):
            create_flow_pcap(dirname, filename)

def filter_pcap(dirname, pcap, time, port, ip):
    print ip, port
    try:
        pkts = rdpcap(dirname + '/' + pcap)
    except IOError as e:
        print e.args
        return
    filtered = (pkt for pkt in pkts if
                TCP in pkt
                and (pkt[TCP].sport == port or pkt[TCP].dport == port)
                and (pkt[IP].dst == ip or pkt[IP].src == ip))
    wrpcap(dirname + '/' + ip + '_' + time + '_filtered_port_num_' + str(port) + '.pcap', filtered)
    # for pkt in pkts:
    #     if TCP in pkt:
    #         if pkt[TCP].sport == port or pkt[TCP].dport == port:
    #             print 'Found'

    # print 'done'

def create_flow_pcap(dirname, filename):
    pcap = filename
    txtname = filename.split('pcap')[0] + 'txt'
    print dirname
    try:
        txt = open(dirname + '/' + txtname, 'r')
    except:
        os.popen('parse_pcap ' + dirname + '/' + pcap + ' > ' + dirname + '/' + txtname)
        txt = open(dirname + '/' + txtname, 'r')
    lines = txt.readlines()
    for line in lines:
        if re.search('\] -- -- --> \[', line):
            port = int(line.split(':')[1].split(']')[0])
            ip = line.split(':')[1].split(']')[1].split('[')[1]
            if re.search('07', filename):
                time = '07' + filename.split('07')[1].split('.')[0]
                try:
                    filter_pcap(dirname, pcap, time, port, ip)
                except:
                    print filename

def already_app_list(arg, dirname, files):
    appname = dirname.split('/')
    appname = appname[len(appname) - 1]
    if appname not in already_apps:
        already_apps.append(appname)


already_dir = '/home/hao/Documents/Ground/'
already_apps = []
os.path.walk(already_dir, already_app_list, None)
print already_apps

dir = '/home/hao/Documents/potential/2/data'
#outdir = '/home/hao/Documents/potential/1/found'
os.path.walk(dir, visit, None)

