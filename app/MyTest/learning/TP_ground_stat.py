__author__ = 'hao'

import re
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
# handle result from
#  java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.trees.RandomForest -t ~/Dropbox/workspace/app/app/MyTest/learning/train_ui_pcap_allFeature.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/ui_pcap.out

def get_ground_truth(pcapname):
    global noncounter, badcounter, goodcounter
    if re.search('/0/', pcapname):
        # bad flows
        pcapdict[pcapname]['truth'] = '2'
        badcounter += 1
    elif re.search('/1/', pcapname):
        for ad in adlist:
            if re.search(ad, host_pcap[pcapname]):
                pcapdict[pcapname]['truth'] = '2'
                return
        pcapdict[pcapname]['truth'] = '3'
        goodcounter += 1
    else:
        pcapdict[pcapname]['truth'] = '1'
        noncounter += 1

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
    nonTP = 0
    nonFP = 0
    nonFN = 0
    nonTN = 0
    goodTP = 0
    goodFP = 0
    badTP = 0
    badFP = 0
    roc_x = []
    roc_y = []
    truth = []
    prediction = []
    for pcap in pcapdict.keys():
        truth.append(pcapdict[pcap]['truth'])
        prediction.append(pcapdict[pcap]['predicted'])
        #print pcap, pcapdict[pcap]['truth'], pcapdict[pcap]['predicted'], host_pcap[pcap]

    # make confusion matrix
    confusionmatrix = Counter()
    for t, p in zip(truth, prediction):
        confusionmatrix[t,p] += 1

    # print confusion matrix
    labels = set(truth + prediction)
    print "t/p",
    for p in sorted(labels):
        print p,
    print
    for t in sorted(labels):
        print t,
        for p in sorted(labels):
            print confusionmatrix[t,p],
        print



    print confusion_matrix(truth, prediction)

    FP1 = float(confusionmatrix['2', '1'] + confusionmatrix['3', '1'])
    TN1 = float(confusionmatrix['2', '2'] + confusionmatrix['2', '3'] + confusionmatrix['3', '2'] + confusionmatrix['3', '3'])
    FPR1 = FP1/(TN1 + FP1)
    print 'FP1: ' + str(FPR1)

    FP2 = float(confusionmatrix['1', '2'] + confusionmatrix['3', '2'])
    TN2 = float(confusionmatrix['1', '1'] + confusionmatrix['1', '3'] + confusionmatrix['3', '1'] + confusionmatrix['3', '3'])
    FPR2 = FP2/(TN2 + FP2)
    print 'FP2: ' + str(FPR2)
    FP3 = float(confusionmatrix['1', '3'] + confusionmatrix['2', '3'])
    TN3 = float(confusionmatrix['1', '1'] + confusionmatrix['1', '2'] + confusionmatrix['2', '1'] + confusionmatrix['2', '2'])
    FPR3 = FP3/(TN3 + FP3)
    print 'FP3: ' + str(FPR3)
    N1 = (confusionmatrix['1', '1'] + confusionmatrix['1', '2'] + confusionmatrix['2', '1'])
    N2 = (confusionmatrix['2', '1'] + confusionmatrix['2', '2'] + confusionmatrix['2', '3'])
    N3 = (confusionmatrix['3', '1'] + confusionmatrix['3', '2'] + confusionmatrix['3', '3'])
    N = N1 + N2 + N3
    W1 = float(N1) / N
    W2 = float(N2) / N
    W3 = float(N3) / N
    print W1, W2, W3
    FPALL = FPR1 * W1 + FPR2 * W2 + FPR3 * W3

    print 'FPAll:' + str(FPALL)

    print(classification_report(truth, prediction))
    #plt.plot(nonFPrate,nonTPrate)
    #plt.show()

    #print float(f_noncounter)/float(noncounter), float(f_badcounter)/float(badcounter), float(f_goodcounter)/float(goodcounter)
    print noncounter, badcounter, goodcounter

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
ui_pcap_out = './ui_pcap_stat.out'
inconsistent = []
noncounter = 0
goodcounter = 0
badcounter = 0
out_handlers(ui_pcap_out)

#print pcapdict

count_host()
print host_count
#for host in sorted(host_count, key=host_count.get, reverse=False):
 #   print host, host_count[host]
find_inconsistent()
print len(pcapdict), len(inconsistent)
print 1 - float(len(inconsistent)) / float(len(pcapdict))

