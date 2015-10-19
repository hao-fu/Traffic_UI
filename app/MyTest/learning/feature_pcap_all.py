__author__ = 'hao'
import csv
import numpy
from statistics import *
import re
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def stat_fea_cal(x):
    return [min(x), max(x), mean(x), median(x), s_dev(x), skewness(x), kurtosis(x)]

def weka_header(stat_num):
    stat_name = ['min', 'max', 'mean', 'median', 'sdev', 'skewness', 'kurtosis']
    train_file.write('@RELATION ' + 'pcap' + '\n')
    train_file.write('@ATTRIBUTE frameNum NUMERIC\n')
    for i in range(stat_num):
        train_file.write('@ATTRIBUTE frameStat_' + stat_name[i] + ' NUMERIC\n')
    for i in range(stat_num):
        train_file.write('@ATTRIBUTE epoStat_' + stat_name[i] + ' NUMERIC\n')
    for i in range(stat_num):
        train_file.write('@ATTRIBUTE upStat_' + stat_name[i] + ' NUMERIC\n')
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
    # print s_ports
    if re.search('/1', dirname):
        fea_val['class'] = 1
    elif re.search('/0', dirname):
        fea_val['class'] = 0
    else:
        fea_val['class'] = 2
    #weka_data(fea_val)
    #fea_val_list.append(fea_val)

def get_data(dir):
    titles = []
    titles_label = []
    #fea_val = {}
    os.path.walk(dir, visit, [titles, titles_label])
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
    weka_header(7)
    # For each, print the vocabulary word and the number of times it appears in the training set
    for tag, count in zip(vocab, dist):
        #print '@ATTRIBUTE word_freq_' + tag + ' NUMERIC'
        train_file.write('@ATTRIBUTE word_freq_' + tag.encode('utf-8') + ' NUMERIC\n')
        #print count

    train_file.write('@ATTRIBUTE class {0, 1}\n')
    #print '\n@DATA'
    train_file.write('\n@DATA\n')

    if len(titles_label) != len(fea_val_list):
        print len(fea_val_list), len(titles_label)
        print 'ERROR: number of titles and fea_val not consistent'
        exit(1)
    counter = 0
    for title_counts in train_data_features:
        if len(fea_val_list[counter]) < 7:
            counter += 1
            continue
        weka_data(fea_val_list[counter])
        # print title_counts
        #word_freq_list = []
        for word_count in title_counts:
            # calculate freq of words = percentage of words in front page that match WORD
            # i.e. 100 * (number of times the WORD appears in the front_page) /  total number of words in front page
            word_freq = 100 * float(word_count) / float(total_words)
            #word_freq_list.append(word_freq)
            #sys.stdout.write(str(word_freq) + ',')
            train_file.write(str(word_freq) + ',')
        #sys.stdout.write(str(titles_lable[counter]) + '\n')
        train_file.write(str(titles_label[counter]) + '\n')
        counter += 1

def str2words(str, wordlist):
    #print 'English Detected!'
    str = re.sub('(http|com|net|org|/|\?|=|_|:|&|\.)', ' ', str)  # if English only
    words = str.lower().split()
    #words = [w for w in words if not w in stopwords.words("english")]
    #print words

    # print '/'.join(words) #  do not use print if you want to return
    for word in words:
        if len(word) < 11:
            wordlist.append(word)
    return ' '.join(words)

# read from txt and get url
def struct_fea_cal(dirname, filename, titles, titles_label):
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
    for uri in uris:
        if uri:
            urilist.append(uri)
            if uri not in distinct_uri:
                distinct_uri.append(uri)
            print uri
            host = uri.split('/')[2]
            if host not in domain_list:
                domain_list.append(host)
            # ignore the parameter part of URI
            #uri = uri.split['?'][0]
            str2words(uri, wordlist)
            break

    titles.append(' '.join(wordlist))
    if re.search('/0', dirname):
        titles_label.append(0)
    else:
        titles_label.append(1)
    return True

def visit(arg, dirname, files):
    titles = arg[0]
    titles_label = arg[1]
    for filename in files:
        if re.search('\.csv', filename) or (re.search('\.c1sv', filename) and re.search('/0', dirname)):
            
            if struct_fea_cal(dirname, filename, titles, titles_label):
                fea_val = {}
                sta_fea_cal(dirname, filename, fea_val)
                fea_val_list.append(fea_val)


#dir = '/home/hao/Dropbox/Descrption-to-traffic/pcap'
#dir = '/home/hao/Documents/pcap'
#dir = '/home/hao/Documents/Ground'
dir = '/home/hao/Documents/pcap2' # to see whether loc or not
fea_val_list = []
#train_file = open('train_pcap.arff', 'w')
#train_file = open('train_pcap_allFeature.arff', 'w')
train_file = open('train_pcap2_allFeature.arff', 'w')
urilist = []
distinct_uri = []
domain_list = []
get_data(dir)
train_file.close()


print domain_list
print len(domain_list)


