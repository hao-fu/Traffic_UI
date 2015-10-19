__author__ = 'hao'
# input prediction results of many classifiers, then do voting on the predicted instances

import csv
import os
import re

def csv_handlers(dirname, filename):
    csvreader = csv.DictReader(open(dirname + '/' + filename, 'rb'), delimiter=',')
    result = []
    for row in csvreader:
        result.append(row['predicted'])
    return result#map(str, result[:, 2].tolist())

def visit(arg, dirname, files):
    global RF, NB
    for filename in files:
        if re.search('RF\.csv', filename):
            RF = csv_handlers(dirname, filename)
        if re.search('NB\.csv', filename):
            NB = csv_handlers(dirname, filename)




def get_data(dir):
    os.path.walk(dir, visit, None)
    if len(RF) != len(NB):
        print 'ERROR'
        exit(1)
    if len(NB) != len(ui_dir):
        print 'ERROR: '
        print len(NB)
        print NB
        exit(1)
    for i in range(len(RF)):
        if RF[i] != NB[i]:
             non_consist_list.append(i)
    print RF
    print NB
    print non_consist_list

RF = [] # random forest
NB = [] # naive bayes
dir = '.'
non_consist_list = []
ui_dir_file = open('ui_instance_map.txt', 'r')
ui_dir = ui_dir_file.readlines()
print len(ui_dir)
get_data(dir)
print len(RF)
print len(non_consist_list)
print float(len(non_consist_list)) / float(len(RF))
for i in range(len(non_consist_list)):
    print ui_dir[i]
