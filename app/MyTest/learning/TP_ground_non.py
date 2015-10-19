__author__ = 'hao'

import re
import json

# handle result from
#  java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.trees.RandomForest -t ~/Dropbox/workspace/app/app/MyTest/learning/train_ui_pcap_allFeature.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/ui_pcap.out

def get_ground_truth(pcapname):
    if re.search('/non-Loc/', pcapname):
        pcapdict[pcapname]['truth'] = '1'
        non_loc_list.append(pcapdict[pcapname])
    elif re.search('/0/', pcapname):
        pcapdict[pcapname]['truth'] = '2'
        bad_loc_list.append(pcapdict[pcapname])
    else:
        for ad in adlist:
            if re.search(ad, host_pcap[pcapname]):
                pcapdict[pcapname]['truth'] = '2'
                bad_loc_list.append(pcapdict[pcapname])
                return
        pcapdict[pcapname]['truth'] = '3'
        good_loc_list.append(pcapdict[pcapname])

def out_handlers(ui_pcap_out):
    file = open(ui_pcap_out, 'rb')
    lines = file.readlines()
    for line in lines:
        if re.search('1', line) and not re.search('predicted error', line):
            pcapname = line.split('(')[1].split(')')[0]
            # get ui label and predicted label
            pcapdict[pcapname] = {}
            pcapdict[pcapname]['ui_label'] = line.split('        ')[1].split(':')[0]
            pcapdict[pcapname]['predicted'] = line.split('        ')[2].split(':')[0]
            #pcapdict[pcapname] = [line.split('        ')[1].split(':')[0], line.split('        ')[2].split(':')[0]]
            get_ground_truth(pcapname)

def find_inconsistent():
    for pcap in pcapdict.keys():
        #print pcap, pcapdict[pcap]['truth'], pcapdict[pcap]['predicted'], host_pcap[pcap]
        if pcapdict[pcap]['truth'] != pcapdict[pcap]['predicted']:
            print pcap, pcapdict[pcap]['truth'], pcapdict[pcap]['predicted'], host_pcap[pcap]
            inconsistent.append(pcap)
            if pcapdict[pcap]['truth'] == '2':
                error_bad.append(pcapdict[pcap])
            elif pcapdict[pcap]['truth'] == '3':
                error_good.append(pcapdict[pcap])
            else:
                error_non.append(pcapdict[pcap])


def count_host():
    for pcap in host_pcap:
        if host_pcap[pcap] not in host_count.keys():
            host_count[host_pcap[pcap]] = 1
        else:
            host_count[host_pcap[pcap]] += 1



host_count = {}
pcapdict = {}
adlist = ['talkingdata', 'easemob', 'appx.91', 'ads', 'share.mob', 'flurry', 'umeng', 'chinacloud',
          'domob', 'scorecard', 'mobvoi', 'bmob', 'igeak', 'wirelessdeve', 'apps123', 'ixingji.com'
          ,'analytics', 'lizhi', 'ynuf.alipay.com', 'kiip', 'appspot', 'openspeech', 'tuisong', 'igexin'
          ,'wapx', 'push']
host_pcap = json.load(open('pcap_host.json', 'r'))
ui_pcap_out = './ui_pcap_non.out'
inconsistent = []
non_loc_list = []
bad_loc_list = []
good_loc_list = []
error_bad = []
error_good = []
error_non = []
out_handlers(ui_pcap_out)
find_inconsistent()

#print pcapdict

count_host()
print host_count
for host in sorted(host_count, key=host_count.get, reverse=False):
    print host, host_count[host]
print len(pcapdict), len(inconsistent)
print (1 - float(len(inconsistent)) / float(len(pcapdict))) * 100
print 'TP of bad flows: ' + str((1 - float(len(error_bad)) / float(len(bad_loc_list))) * 100)
print 'TP of good flows: ' + str((1 - float(len(error_good)) / float(len(good_loc_list)))* 100)
print 'TP of non-Loc flows: ' + str((1 - float(len(error_non)) / float(len(non_loc_list)))* 100)
