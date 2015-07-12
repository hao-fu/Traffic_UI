__author__ = 'hao'

import os
import re

def visit(arg, dirname, files):
    for filename in files:
        if re.search(r'pcap', filename):
            txt = filename.split('pcap')[0] + 'csv'
            os.popen('./pcap2csv.sh ' + dirname + '/' + filename + ' ' + dirname + '/' + txt)


dir = '/home/hao/Documents/ads'
os.path.walk(dir, visit, None)