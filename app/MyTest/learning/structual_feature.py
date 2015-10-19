import re
import os
import csv
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def weka(vocab, dist, train_data_features, total_words, titles_label):
    arffname = 'uri_structure'
    # save to arff
    #print '@RELATION ' + arffname
    train_file.write('@RELATION ' + arffname + '\n')
    # For each, print the vocabulary word and the number of times it appears in the training set
    for tag, count in zip(vocab, dist):
        #print '@ATTRIBUTE word_freq_' + tag + ' NUMERIC'
        train_file.write('@ATTRIBUTE word_freq_' + tag.encode('utf-8') + ' NUMERIC\n')
        #print count
    train_file.write('@ATTRIBUTE class {0, 1}\n')
    #print '\n@DATA'
    train_file.write('\n@DATA\n')

    counter = 0
    for title_counts in train_data_features:
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
def fea_cal(dirname, filename, titles, titles_label):
    pcapreader = csv.reader(open(dirname + '/' + filename, 'rb'), delimiter='\t')
    result = list(pcapreader)
    result = np.array(result)
    wordlist = []
    try:
        uris = result[:, 26]
    except IndexError as e:
        print e.args
        print e.message
        return
    for uri in uris:
        if uri:
            urilist.append(uri)
            if uri not in distinct_uri:
                distinct_uri.append(uri)
            print uri
            # ignore the parameter part of URI
            #uri = uri.split['?'][0]
            str2words(uri, wordlist)
            break
    titles.append(' '.join(wordlist))
    if re.search('/0', dirname):
        titles_label.append(0)
    else:
        titles_label.append(1)



def visit(arg, dirname, files):
    titles = arg[0]
    titles_label = arg[1]
    for filename in files:
        if re.search('.csv', filename):
            fea_cal(dirname, filename, titles, titles_label)


def get_data(dir):
    titles = []
    titles_label = []
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
    weka(vocab, dist, train_data_features, total_words, titles_label)

urilist = []
distinct_uri = []
dir = '/home/hao/Documents/pcap'
train_file = open('train_pcap_struc.arff', 'w')
get_data(dir)
print 'total uri: ' + str(len(urilist))
print 'distinct uri: ' + str(len(distinct_uri))
