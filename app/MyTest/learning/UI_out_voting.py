__author__ = 'hao'
# input prediction results of many classifiers, then do voting on the predicted instances
#java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.bayes.NaiveBayes -t ~/Dropbox/workspace/app/app/MyTest/train_UI.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/UI_predict_NB.out
#java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W  weka.classifiers.trees.RandomForest -t ~/Dropbox/workspace/app/app/MyTest/train_UI.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/UI_predict_RF.out

import os
import re
import json

def out_handlers(dirname, filename):
    file = open(dirname + '/' + filename, 'rb')
    lines = file.readlines()
    result = {}
    for line in lines:
        if re.search('1', line) and not re.search('predicted error', line):
            appname = line.split('(')[1].split(')')[0]
            if appname not in applist:
                applist.append(appname)
            if appname in result.keys():
                if result[appname][0] != result[appname][1]:
                    result[appname] = [line.split('        ')[1].split(':')[0], line.split('        ')[2].split(':')[0]]
            else:
                result[appname] = [line.split('        ')[1].split(':')[0], line.split('        ')[2].split(':')[0]]
    return result#map(str, result[:, 2].tolist())

def visit(arg, dirname, files):
    global RF, NB, LG
    for filename in files:
        if re.search('RF\.out', filename):
            RF = out_handlers(dirname, filename)
        elif re.search('NB\.out', filename):
            NB = out_handlers(dirname, filename)
        elif re.search('LG\.out', filename):
            LG = out_handlers(dirname, filename)

def get_data(dir):
    os.path.walk(dir, visit, None)
    if len(RF) != len(NB) or len(LG) != len(NB):
        print 'ERROR'
        exit(1)
    # if len(NB) != len(ui_dir):
    #     print 'ERROR: '
    #     print len(NB)
    #     print NB
    #     exit(1)
    #for i in range(len(RF)):
        # if RF[i] != NB[i]:
        #      non_consist_list.append(i)
    for app in applist:
        print app
        if RF[app] == NB[app] and NB[app] == LG[app]:
            consist_dict[app] = RF[app]
        else:
            print RF[app]
            print NB[app]
    print RF
    print NB
    print LG
    print consist_dict

RF = {}  # random forest
NB = {}  # naive bayes
LG = {}  # logistic
dir = '.'
applist = []
consist_dict = {}
#ui_dir_file = open('ui_instance_map.txt', 'r')
#ui_dir = ui_dir_file.readlines()
#print len(ui_dir)
get_data(dir)
print len(RF),len(applist)
print len(consist_dict)
print 1 - float(len(consist_dict)) / float(len(RF))
counter = 0
json.dump(consist_dict, open('ui_pcap_label.json', 'w'))
miss_bad = 0
total_bad = 0
for app in consist_dict.keys():
    if consist_dict[app][0] == '1':
        total_bad += 1
    if consist_dict[app][0] != consist_dict[app][1]:
        print app
        if consist_dict[app][0] == '1':
            miss_bad += 1
        counter += 1
#for i in range(len(non_consist_list)):
    #print ui_dir[i]
print len(consist_dict) - total_bad, total_bad
print 1 - float(miss_bad) / float(total_bad), 1 - float(counter - miss_bad) / float(len(consist_dict) - total_bad)
print 1 - float(counter) / float(len(consist_dict))
