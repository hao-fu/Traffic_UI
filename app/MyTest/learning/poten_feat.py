__author__ = 'hao'
import csv
import numpy
from statistics import *
import re
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import json

def stat_fea_cal(x):
    return [min(x), max(x), mean(x), median(x), s_dev(x), skewness(x), kurtosis(x)]

def weka_header(stat_num):
    stat_name = ['min', 'max', 'mean', 'median', 'sdev', 'skewness', 'kurtosis']
    train_file.write('@RELATION ' + 'pcap' + '\n')
    train_file.write('@ATTRIBUTE pcapname STRING\n')
    train_file.write('@ATTRIBUTE frameNum NUMERIC\n')
    for i in range(stat_num):
        train_file.write('@ATTRIBUTE frameStat_' + stat_name[i] + ' NUMERIC\n')
    for i in range(stat_num):
        train_file.write('@ATTRIBUTE epoStat_' + stat_name[i] + ' NUMERIC\n')
    for i in range(stat_num):
        train_file.write('@ATTRIBUTE upStat_' + stat_name[i] + ' NUMERIC\n')
    for i in range(stat_num):
        train_file.write('@ATTRIBUTE downStat_' + stat_name[i] + ' NUMERIC\n')
    train_file.write('@ATTRIBUTE non_httpFrameNum NUMERIC\n')
    train_file.write('@ATTRIBUTE upCounter NUMERIC\n')
    #train_file.write('@ATTRIBUTE class {0, 1, 2}\n')
    #train_file.write('\n@DATA\n')


def weka_data(fea_val):
    train_file.write(str(fea_val['frameNum']) + ',')
    for i in fea_val['frameStat']:
        train_file.write(str(i) + ',')
    for i in fea_val['epoStat']:
        train_file.write(str(i) + ',')
    for i in fea_val['upStat']:
        train_file.write(str(i) + ',')
    for i in fea_val['downStat']:
        train_file.write(str(i) + ',')
    train_file.write(str(fea_val['non_httpFrameNum']) + ',')
    train_file.write(str(fea_val['upCounter']) + ',')
    #train_file.write(str(fea_val['class']) + '\n')


def sta_fea_cal(dirname, filename, fea_val):
    pcapreader = csv.reader(open(dirname + '/' + filename, 'rb'), delimiter='\t')
    result = list(pcapreader)
    result = numpy.array(result)
    # print result
    fea_val['frameNum'] = len(result)
    print fea_val['frameNum']
    try:
        frame_len = map(int, result[:, 1].tolist())
    except:
        print dirname
        return
    fea_val['frameStat'] = stat_fea_cal(frame_len)
    print fea_val['frameStat']

    epoch = map(float, result[:, 63].tolist())
    interval = []
    for i in range(1, len(epoch)):
        interval.append(epoch[i] - epoch[i - 1])
    # print interval
    fea_val['epoStat'] = stat_fea_cal(interval)
    print fea_val['epoStat']

    protos = map(str, result[:, 2].tolist())
    http_counter = 0
    for prot in protos:
        if re.search('http', prot):
            http_counter += 1
    fea_val['non_httpFrameNum'] = fea_val['frameNum'] - http_counter
    print fea_val['non_httpFrameNum']

    # uplink and downlink
    try:
        s_ports = map(int, result[:, 6].tolist())
    except:
        fea_val = {}
        return
    d_ports = map(int, result[:, 7].tolist())
    port_s = s_ports[0]
    # port_d = d_ports[0]
    up_frames = []
    for i in range(len(s_ports)):
        if s_ports[i] == port_s:
            up_frames.append(frame_len[i])
    fea_val['upCounter'] = len(up_frames)
    print fea_val['upCounter']
    fea_val['upStat'] = stat_fea_cal(up_frames)

    d_ports = map(int, result[:, 7].tolist())
    port_d = d_ports[0]
    down_frames = []
    for i in range(len(d_ports)):
        if d_ports[i] != port_d:
            down_frames.append(frame_len[i])
    fea_val['downStat'] = stat_fea_cal(down_frames)
    # print s_ports
    # if re.search('/1', dirname):
    #     fea_val['class'] = 1
    # elif re.search('/0', dirname):
    #     fea_val['class'] = 0
    # else:
    #     fea_val['class'] = 2
    #weka_data(fea_val)
    #fea_val_list.append(fea_val)

def get_data(dir):
    titles = []
    titles_label = []
    titles_dir = []
    #fea_val = {}
    os.path.walk(dir, visit, [titles, titles_label, titles_dir])

    # Initialize the "CountVectorizer" object, which is scikit-learn's bag of words tool.


    if len(titles_label) != len(titles) or len(titles_dir) != len(titles):
        print 'ERROR: number of titles and titles not consistent'
        exit(1)
    weka(titles, titles_label, titles_dir)

def weka(titles, titles_label, titles_dir):
    weka_header(7)
    # For each, print the vocabulary word and the number of times it appears in the training set

    if numeric_flag:
        for word in vocabulary:
            #print '@ATTRIBUTE word_freq_' + tag + ' NUMERIC'
            train_file.write('@ATTRIBUTE word_freq_' + word + ' NUMERIC\n')
    else:
        for word in vocabulary:
            #print '@ATTRIBUTE word_freq_' + tag + ' NUMERIC'
            train_file.write('@ATTRIBUTE word_freq_' + word + ' {0, 1}\n')
            #print count

    train_file.write('@ATTRIBUTE class {0, 1, 2}\n')
    #print '\n@DATA'
    train_file.write('\n@DATA\n')

    if len(titles_label) != len(fea_val_list):
        print len(fea_val_list), len(titles_label)
        print 'ERROR: number of titles and fea_val not consistent'
        exit(1)
    counter = 0
    for title in titles:
        if len(fea_val_list[counter]) < 6:
            counter += 1
            continue
        train_file.write(titles_dir[counter] + ',')
        weka_data(fea_val_list[counter])
        # print title_counts
        #word_freq_list = []
        for word_count in title:
              # calculate freq of words = percentage of words in front page that match WORD
            # i.e. 100 * (number of times the WORD appears in the front_page) /  total number of words in front page

            #word_freq_list.append(word_freq)
            #sys.stdout.write(str(word_freq) + ',')
                if int(word_count) > 0:
                    train_file.write('1,')
                else:
                    train_file.write('0,')
        #sys.stdout.write(str(titles_lable[counter]) + '\n')
        train_file.write(str(titles_label[counter]) + '\n')
        counter += 1

def str2words(str, title):
    if re.search('(png|jpg|gif)', str):
            return False
    #print 'English Detected!'
    str = re.sub('(http|com|net|org|/|\?|=|_|:|&|\.)', ' ', str)  # if English only
    words = str.lower().split()
    #words = [w for w in words if not w in stopwords.words("english")]
    #print words

    # print '/'.join(words) #  do not use print if you want to return
    flag = False
    for word in words:
        if len(word) < 13:
            for i in range(len(vocabulary)):
                if word.encode('utf-8') == vocabulary[i]:
                    title[i] += 1
                    if vocabulary[i] in vocabulary_few:
                        flag = True
                    break
            #if not flag:
             #   return flag
            #if word not in vocabulary:
            #    title[len(vocabulary)] = 1
    return flag

# read from txt and get url
def struct_fea_cal(dirname, filename, titles, titles_label, titles_dir):
    #print 'label:' + str(ui_label)
    pcapreader = csv.reader(open(dirname + '/' + filename, 'rb'), delimiter='\t')
    result = list(pcapreader)
    result = np.array(result)
    title = []
    try:
        uris = result[:, 26]
    except IndexError as e:
        print e.args
        print e.message
        return False
    host = None
    for uri in uris:
        if uri:
            title = [0] * (len(vocabulary))
            urilist.append(uri)
            if uri not in distinct_uri:
                distinct_uri.append(uri)
            print uri
            host = uri.split('/')[2]

            host_pcap[dirname + '/' + filename] = host
            if host not in domain_list:
                domain_list.append(host)
            # ignore the parameter part of URI
            #uri = uri.split['?'][0]
            if not str2words(uri, title):
                return False
            break
    if len(title) == 0:
        return False

    titles.append(title)
    titles_label.append('0')
    titles_dir.append(dirname + '/' + filename)
    return True

def visit(arg, dirname, files):
    titles = arg[0]
    titles_label = arg[1]
    titles_dir = arg[2]
    for filename in files:
        if re.search('\.csv', filename) or (re.search('\.c1sv', filename) and re.search('/0', dirname)):
            global total_pcap
            total_pcap += 1
            if struct_fea_cal(dirname, filename, titles, titles_label, titles_dir):
                fea_val = {}
                sta_fea_cal(dirname, filename, fea_val)
                fea_val_list.append(fea_val)


#dir = '/home/hao/Dropbox/Descrption-to-traffic/pcap'
#dir = '/home/hao/Documents/pcap'
#dir = '/home/hao/Documents/Ground'

host_pcap = {}
fea_val_list = []
numeric_flag = False
total_pcap = 0
#vocabulary = json.load(open('train_ocsvm_vocab.json', 'r'))
vocabulary = json.load(open('train_vocab.json', 'r'))
print len(vocabulary) + 32
vocabulary_txt = open('word_feat.txt', 'r')
vocabulary_txt = vocabulary_txt.readlines()
vocabulary_few = []
for voca in vocabulary_txt:
    vocabulary_few.append(voca.split('\n')[0])
#print vocabulary_few
train_file = open('poten_pcap_all.arff', 'w')
urilist = []
distinct_uri = []
domain_list = []
dir = '/home/hao/Documents/potential/'
get_data(dir)
train_file.close()
json.dump(host_pcap, open('poten_pcap_host_test.json', 'w'))

print domain_list
print len(domain_list)
print total_pcap

#os.popen('java weka.core.converters.CSVSaver -i test_ui_pcap_ocsvm_all.arff -o test_ui_pcap_ocsvm_all.csv')


