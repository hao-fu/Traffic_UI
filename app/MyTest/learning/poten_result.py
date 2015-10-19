__author__ = 'hao'

import re
import csv
import numpy as np

txt = open('poten_feat.out', 'r')
lines = txt.readlines()
applist = []
for line in lines:
    if re.search('   \+   ', line):
        pcap = line.split('(')[1].split(')')[0]
        pcapreader = csv.reader(open(pcap, 'rb'), delimiter='\t')
        result = list(pcapreader)
        result = np.array(result)
        title = []
        try:
            uris = result[:, 26]
        except IndexError as e:
            print e.args
            print e.message
        host = None
        for uri in uris:
            if uri:
                if re.search('2\:1', line):
                    prediction = 'bad, '
                else:
                    prediction = 'good,  '
                print uri + ': ' + prediction + pcap
                app = pcap.split('/')
                app = app[len(app) - 2]
                if app not in applist:
                    applist.append(app)
                host = uri.split('/')[2]
                break
print applist
print len(applist)
print len(lines)