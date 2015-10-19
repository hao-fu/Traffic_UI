# -*- coding: utf-8 -*-
__author__ = 'hao'

from scapy.layers.inet import IP, TCP
from scapy.all import *
import os
import re


def filter_pcap(dirname, pcap, time, iptable):
    try:
        pkts = rdpcap(dirname + '/' + pcap)
    except IOError as e:
        print e.args
        return
    for ip in iptable:
        filtered = (pkt for pkt in pkts if
                TCP in pkt
                and (pkt[TCP].sport in ports or pkt[TCP].dport in ports)
                and (pkt[IP].dst in ip or pkt[IP].src in ip))
        wrpcap(dirname + '/' + ip + '_' + time + '_filtered.pcap', filtered)
    print 'done'

def visit(arg, dirname, files):
    print dirname
    for filename in files:
        if re.search(r'.*?-.*?-.*?log', filename):
            print filename
            iptable = []
            file = open(dirname + '/' + filename, 'r')
            lines = file.readlines()
            for line in lines:
                if re.search('.*?Location.*?', line):
                    line = line.split(', ')[1]
                    if line not in iptable:
                        iptable.append(line)
            pcap = dirname.split('/')
            if re.search('.*?apk.*?', filename):
                time = filename.split('apk')[1].split('.')[0]
            else:
                if re.search('070', filename):
                    time = '070' + filename.split('070')[1].split('.')[0]
                elif re.search('06', filename):
                    #time = '06' + filename.split('06')[1].split('.')[0]
                    time = ''
            pcap = pcap[len(pcap) - 1] + time + '.pcap'
            filter_pcap(dirname, pcap, time, iptable)

ports = [80, 8080]
dir = '/home/hao/Documents/Loc'
os.path.walk(dir, visit, None)
