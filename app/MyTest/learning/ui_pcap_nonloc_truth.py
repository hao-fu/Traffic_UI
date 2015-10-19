__author__ = 'hao'
import csv
import numpy
from statistics import *
import re
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import json
import random

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

    # test_file.write('@RELATION ' + 'pcap' + '\n')
    # test_file.write('@ATTRIBUTE pcapname STRING\n')
    # test_file.write('@ATTRIBUTE frameNum NUMERIC\n')
    # for i in range(stat_num):
    #     test_file.write('@ATTRIBUTE frameStat_' + stat_name[i] + ' NUMERIC\n')
    # for i in range(stat_num):
    #     test_file.write('@ATTRIBUTE epoStat_' + stat_name[i] + ' NUMERIC\n')
    # for i in range(stat_num):
    #     test_file.write('@ATTRIBUTE upStat_' + stat_name[i] + ' NUMERIC\n')
    # test_file.write('@ATTRIBUTE non_httpFrameNum NUMERIC\n')
    # test_file.write('@ATTRIBUTE upCounter NUMERIC\n')


def weka_data(fea_val):
    train_file.write(str(fea_val['pcap']) + ',')
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

def test_weka_data(fea_val):
    test_file.write(str(fea_val['pcap']) + ',')
    test_file.write(str(fea_val['frameNum']) + ',')
    for i in fea_val['frameStat']:
        test_file.write(str(i) + ',')
    for i in fea_val['epoStat']:
        test_file.write(str(i) + ',')
    for i in fea_val['upStat']:
        test_file.write(str(i) + ',')
    for i in fea_val['downStat']:
        train_file.write(str(i) + ',')
    test_file.write(str(fea_val['non_httpFrameNum']) + ',')
    test_file.write(str(fea_val['upCounter']) + ',')


def sta_fea_cal(dirname, filename, fea_val):
    pcapreader = csv.reader(open(dirname + '/' + filename, 'rb'), delimiter='\t')
    result = list(pcapreader)
    result = numpy.array(result)
    # print result
    fea_val['pcap'] = dirname + '/' + filename
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

    port_s = s_ports[0]
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

def get_data(txt):
    titles = []
    titles_label = []
    #fea_val = {}
    appdict = json.load(open(txt, 'r'))
    #appdict = eval(ui_label_txt)
    # for loc data
    for appdir in appdict.keys():
        if re.search('/0/', appdir):
            os.path.walk(appdir, visit, [titles, titles_label, '1'])
        elif re.search('/1/', appdir):
            os.path.walk(appdir, visit, [titles, titles_label, '2'])
    os.path.walk(non_loc_dir, visit, [titles, titles_label, 0]) # for non-loc data
    # Initialize the "CountVectorizer" object, which is scikit-learn's bag of words tool.
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)
    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
    titles_vocab_mat = vectorizer.fit_transform(titles)
    # Numpy arrays are easy to work with, so convert the result to an array
    #print vectorizer.vocabulary_  # a dict, the value is the index
    train_data_features = titles_vocab_mat.toarray()
    print train_data_features.shape
    # Take a look at the words in the vocabulary
    vocab = vectorizer.get_feature_names()
    print '/'.join(vocab)
    # Sum up the counts of each vocabulary word
    dist = np.sum(train_data_features, axis=0)
    total_words = 0
    for i in train_data_features:
        #print sum(i)
        total_words += sum(i)
    print total_words
    if len(titles_label) != len(titles):
        print 'ERROR: number of titles and titles not consistent'
        exit(1)
    weka(vocab, dist, train_data_features, total_words, titles_label)

def weka(vocab, dist, train_data_features, total_words, titles_label):
    if len(titles_label) != len(fea_val_list):
        print len(fea_val_list), len(titles_label)
        print 'ERROR: number of titles and fea_val not consistent'
        exit(1)
    weka_header(7)
    # For each, print the vocabulary word and the number of times it appears in the training set
    if numeric_flag:
        for tag, count in zip(vocab, dist):
            #print '@ATTRIBUTE word_freq_' + tag + ' NUMERIC'
            train_file.write('@ATTRIBUTE word_freq_' + tag.encode('utf-8') + ' NUMERIC\n')
            test_file.write('@ATTRIBUTE word_freq_' + tag.encode('utf-8') + ' NUMERIC\n')
    else:
        for tag, count in zip(vocab, dist):
            #print '@ATTRIBUTE word_freq_' + tag + ' NUMERIC'
            train_file.write('@ATTRIBUTE word_freq_' + tag.encode('utf-8') + ' {0, 1}\n')
            test_file.write('@ATTRIBUTE word_freq_' + tag.encode('utf-8') + ' {0, 1}\n')
            vocabulary.append(tag.encode('utf-8'))
            #print count

    train_file.write('@ATTRIBUTE class {0, 1, 2}\n')
    test_file.write('@ATTRIBUTE class {0, 1, 2}\n')
    #print '\n@DATA'
    train_file.write('\n@DATA\n')
    test_file.write('\n@DATA\n')


    counter = -1
    badcounter = -1
    noncounter = -1
    rand = random.sample(range(1400), 762)
    rand2 = random.sample(range(1000), 800)
    for title_counts in train_data_features:
        test_flag = False
        counter += 1
        if len(fea_val_list[counter]) < 7:
            continue
        if str(titles_label[counter]) == '1':
            badcounter += 1
            #if badcounter > 805:
            #if badcounter not in rand:
                #test_flag = True
        elif str(titles_label[counter]) == '0':
            noncounter += 1
            if noncounter > 850:
                continue
            #if noncounter not in rand2:
                #continue
        if test_flag:
            test_weka_data(fea_val_list[counter])
            for word_count in title_counts:
                # calculate freq of words = percentage of words in front page that match WORD
                # i.e. 100 * (number of times the WORD appears in the front_page) /  total number of words in front page

                #word_freq_list.append(word_freq)
                #sys.stdout.write(str(word_freq) + ',')
                if numeric_flag:
                    word_freq = 100 * float(word_count) / float(total_words)
                    test_file.write(str(word_freq) + ',')
                else:
                    if int(word_count) > 0:
                        test_file.write('1,')
                    else:
                        test_file.write('0,')
        #sys.stdout.write(str(titles_lable[counter]) + '\n')
            test_file.write(str(titles_label[counter]) + '\n')
        else:
            weka_data(fea_val_list[counter])
        # print title_counts
        #word_freq_list = []
            for word_count in title_counts:
                # calculate freq of words = percentage of words in front page that match WORD
                # i.e. 100 * (number of times the WORD appears in the front_page) /  total number of words in front page

                #word_freq_list.append(word_freq)
                #sys.stdout.write(str(word_freq) + ',')
                if numeric_flag:
                    word_freq = 100 * float(word_count) / float(total_words)
                    train_file.write(str(word_freq) + ',')
                else:
                    if int(word_count) > 0:
                        train_file.write('1,')
                    else:
                        train_file.write('0,')
        #sys.stdout.write(str(titles_lable[counter]) + '\n')
            train_file.write(str(titles_label[counter]) + '\n')

def str2words(str, wordlist):
    #print 'English Detected!'
    str = re.sub('(http|com|net|org|/|\?|=|_|:|&|\.)', ' ', str)  # if English only
    words = str.lower().split()
    #words = [w for w in words if not w in stopwords.words("english")]
    #print words

    # print '/'.join(words) #  do not use print if you want to return
    for word in words:
        if len(word) < 13:
            wordlist.append(word)
    return ' '.join(words)

# read from txt and get url
def struct_fea_cal(dirname, filename, titles, titles_label, ui_label):
    pcapreader = csv.reader(open(dirname + '/' + filename, 'rb'), delimiter='\t')
    result = list(pcapreader)
    result = np.array(result)
    wordlist = []
    try:
        uris = result[:, 26]
    except IndexError as e:
        print e.args
        print e.message
        return False
    '''
    if ui_label == 0:
        titles.append(' '.join(wordlist))
        titles_label.append(ui_label)
        return True
    '''
    host = None
    for uri in uris:
        if uri:
            urilist.append(uri)
            if uri not in distinct_uri:
                distinct_uri.append(uri)
            print uri
            if ui_label != 0 and re.search('(jpg|png|gif)', uri):
                return
            host = uri.split('/')[2]

            host_pcap[dirname + '/' + filename] = host
            if host not in domain_list and ui_label != 0:
                domain_list.append(host)
            # ignore the parameter part of URI
            #uri = uri.split['?'][0]
            str2words(uri, wordlist)
            break
    if filter_ad and host and ui_label == "2":
        for ad in adlist:
            if re.search(ad, host):
                return False
                ui_label = 1
                break
    if not host:
        host_pcap[dirname + '/' + filename] = host
    titles.append(' '.join(wordlist))
    titles_label.append(ui_label)
    return True

def visit(arg, dirname, files):
    titles = arg[0]
    titles_label = arg[1]
    ui_label = arg[2]
    for filename in files:
        if re.search('\.csv', filename) or (re.search('\.c1sv', filename) and re.search('/0', dirname)):
            print dirname, filename
            if struct_fea_cal(dirname, filename, titles, titles_label, ui_label):
                fea_val = {}
                sta_fea_cal(dirname, filename, fea_val)
                fea_val_list.append(fea_val)


#dir = '/home/hao/Dropbox/Descrption-to-traffic/pcap'
#dir = '/home/hao/Documents/pcap'
#dir = '/home/hao/Documents/Ground'
ui_label_txt = 'ui_pcap_label.json'  # to see whether loc or not
adlist = ['talkingdata', 'easemob', 'appx.91', 'ads', 'share.mob', 'flurry', 'umeng', 'chinacloud',
          'domob', 'scorecard', 'mobvoi', 'bmob', 'igeak', 'wirelessdeve', 'apps123', 'ixingji.com'
          ,'analytics', 'lizhi', 'ynuf.alipay.com', 'kiip', 'appspot', 'openspeech', 'tuisong', 'igexin'
          ,'wapx', 'push']
filter_ad = True
host_pcap = {}
fea_val_list = []
numeric_flag = False
vocabulary = []
non_loc_dir = '/home/hao/Documents/pcap2/non-Loc'
#train_file = open('train_pcap.arff', 'w')
#train_file = open('train_pcap_allFeature.arff', 'w')
train_file = open('train_ui_pcap_non_allFeature_truth.arff', 'w')
test_file = open('test_ui_pcap__bad.arff', 'w')
urilist = []
distinct_uri = []
domain_list = []
get_data(ui_label_txt)
train_file.close()
test_file.close()
#json.dump(host_pcap, open('pcap_host.json', 'w'))
json.dump(vocabulary, open('train_vocab.json', 'w'))


print domain_list
print len(domain_list)


