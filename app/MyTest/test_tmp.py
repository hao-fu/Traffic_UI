import os
import re
import dpkt

def visit(arg, dirname, files):
    for filename in files:
        if re.search('filter', filename):
            print dirname + '/' + filename
            #if re.search('SSL', filename):
             #   print 'SSL'
            file = open(dirname + '/' + filename)
            pcap = dpkt.pcap.Reader(file)
            for ts, buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)
                ip = eth.data
                tcp = ip.data

                if tcp.dport == 80 and len(tcp.data) > 0:
                    http = dpkt.http.Request(tcp.data)
                    print http.uri
            file.close()

dir = '/home/hao/Documents/Ground/'
#os.path.walk(dir, visit, None)
file = open('/home/hao/Documents/Ground/Leakage/com.jh.APPc105b7e4622a45bcaf20d43597cca32a.news/140.205.142.216_0709-19-44-33_filtered.pcap')
pcap = dpkt.pcap.Reader(file)