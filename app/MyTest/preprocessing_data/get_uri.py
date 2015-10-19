__author__ = 'hao'
import os
import re
import dpkt

def visit(arg, dirname, files):
    for filename in files:
        if re.search('filter', filename) and not re.search('SSL', filename) :
            print '>>>>>>>>>>>>>>>>>' + filename
            #if re.search('SSL', filename):
             #   print 'SSL'
            file = open(dirname + '/' + filename)
            pcap = dpkt.pcap.Reader(file)
            for ts, buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)
                ip = eth.data
                tcp = ip.data

                if tcp.dport == 80 and len(tcp.data) > 0:
                    try:
                        http = dpkt.http.Request(tcp.data)
                        #print http.body
                        #print http.headers

                        full_uri = http.headers['host'] + http.uri
                        if full_uri not in uri_list:
                            uri_list.append(full_uri)
                            #print full_uri
                        if filename.split('_')[0] not in iptable:
                            iptable.append(filename.split('_')[0])
                            print filename.split('_')[0]
                        if http.headers['host'] not in host_list:
                            host_list.append(http.headers['host'])
                            print http.headers['host']
                    except:
                        pass
            file.close()

iptable = []
uri_list = []
host_list = []
dir = '/home/hao/Documents/Ground/'
os.path.walk(dir, visit, None)

print iptable
length = len(iptable)
print len(iptable)

print host_list
print len(host_list)
lengthh = len(host_list)

dir = '/home/hao/Documents/Loc/'
os.path.walk(dir, visit, None)

print iptable
print length
print len(iptable) - length

print host_list
print lengthh
print len(host_list) - lengthh