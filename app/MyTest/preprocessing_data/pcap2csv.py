__author__ = 'hao'

import os
import re

def visit(arg, dirname, files):
    for filename in files:
        if re.search(r'port.*?pcap', filename):
            csv = filename.split('pcap')[0] + 'csv'
            try:
                open(dirname + '/' + csv)
            except:
                os.popen('./pcap2csv.sh ' + dirname + '/' + filename + ' ' + dirname + '/' + csv)


#dir = '/home/hao/Documents/ads'
#dir = '/home/hao/Dropbox/Descrption-to-traffic/pcap/'
#dir = '/home/hao/Documents/pcap/'
#dir = '/home/hao/Documents/Ground/'
#dir = '/home/hao/Documents/pcap2/'
#dir = '/home/hao/Documents/potential/2/data'
dir = '/home/hao/Documents/Loc'
os.path.walk(dir, visit, None)