__author__ = 'hao'

import re
import os
from scapy.layers.inet import IP, TCP
from scapy.all import *

# create sub flow pcap for any pcap
# here focus on non-loc folder

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

def visit(arg, dirname, files):
    for filename in files:
        if re.search('.pcap', filename):
            pcap = filename
            txtname = filename.split('pcap')[0] + 'txt'
            try:
                txt = open(dirname + '/' + txtname, 'r')
            except:
                os.popen('parse_pcap ' + dirname + '/' + pcap + ' > ' + dirname + '/' + txtname)
                txt = open(dirname + '/' + txtname, 'r')
            lines = txt.readlines()
            for line in lines:
                if re.search('-->', line):
                    port = int(line.split(':')[1].split(']')[0])
                    ip = line.split(':')[1].split(']')[1].split('[')[1]
                    if re.search('07', filename):
                        time = '07' + filename.split('07')[1].split('.')[0]
                    try:

                        filter_pcap(dirname, pcap, time, port, ip)
                    except:
                        print filename


#dir = '/media/hao/Hitachi/BaiduApks/software/504/1/non-LOC'
#dir = '/home/hao/Dropbox/Descrption-to-traffic/pcap/2'
#dir = '/home/hao/Documents/non-Loc'
dir = '/media/hao/Hitachi/BaiduApks/software/504/1/LOC/data/'
os.path.walk(dir, visit, None)