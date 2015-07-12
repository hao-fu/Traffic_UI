# -*- coding: utf-8 -*-

# bag-of-word model

import os
import re
import xml.dom.minidom
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import jieba
import sys
#from sklearn.ensemble import RandomForestClassifier

def str2words(str, wordlist):
    str = re.sub('°', 'DegreeMark', str)
    if is_Chinese_inside(str):
        #print 'Chinese Detected!'
        str = re.sub(u'[^\u4e00-\u9fa5]', '', str)
        words = jieba.cut(str, cut_all=False)
        # words = [w for w in words if not w in stopwords.words("chinese")]

    else:
        #print 'English Detected!'
        str = re.sub('[^a-zA-Z]', ' ', str) # if English only
        words = str.lower().split()
        words = [w for w in words if not w in stopwords.words("english")]

    # print '/'.join(words) #  do not use print if you want to return
    for word in words:
        wordlist.append(word)
    return ' '.join(words)

def DFS_xml(node, nodelist, wordlist):
    if node not in nodelist:
        nodelist.append(node)
        try:
            txt = node.getAttribute('text')
            desc = node.getAttribute('content-desc').lower()
            resid = node.getAttribute('resource-id').lower()
            if txt:
                #print txt
                str2words(txt, wordlist)
            elif desc:
                str2words(desc, wordlist)
            elif resid:
                str2words(resid.split('/')[1], wordlist)
            for i in node.childNodes:
                DFS_xml(i, nodelist, wordlist)
        except:
            return

def is_Chinese_inside(content):
    '''
    判断是否是中文需要满足u'[\u4e00-\u9fa5]+'，
    需要注意如果正则表达式的模式中使用unicode，那么
    要匹配的字符串也必须转换为unicode，否则肯定会不匹配。
    '''
    iconvcontent = unicode(content)
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zhPattern.search(iconvcontent)
    res = False
    if match:
        res = True
    return res

def visit(arg, dirname, files):
    titles = arg[0]
    titles_lable = arg[1]
    for filename in files:
        if re.search('hierarchy\.xml', filename):
            print filename + '>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            dom = xml.dom.minidom.parse(dirname + '/' + filename)
            root = dom.documentElement
            nodelist = []
            wordlist = []
            DFS_xml(root, nodelist, wordlist)
            titles.append(' '.join(wordlist))
            if re.search('/0', dirname):
                titles_lable.append(0)
            else:
                titles_lable.append(1)
            print '/'.join(wordlist)
            # titles.append(filename)

def get_data(dir):
    titles = []
    titles_lable = []
    os.path.walk(dir, visit, [titles, titles_lable])
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
        total_words += sum(i)
    print total_words

    arffname = 'front_page'
    # save to arff
    print '@RELATION ' + arffname
    # For each, print the vocabulary word and the number of times it appears in the training set
    for tag, count in zip(vocab, dist):
        print '@ATTRIBUTE word_freq_' + tag + ' NUMERIC'
        #print count
    print '\n@DATA'


    counter = 0
    for title_counts in train_data_features:
        # print title_counts
        #word_freq_list = []
        for word_count in title_counts:
            word_freq = 100 * float(word_count) / float(total_words)
            #word_freq_list.append(word_freq)
            sys.stdout.write(str(word_freq) + ',')
        sys.stdout.write(str(titles_lable[counter]) + '\n')
        counter += 1



#nltk.download() # download text data sets, including stop words
train_dir = '/home/watershed2106/Documents/LOC/samplesLoc/'
get_data(train_dir)


#print "Training the random forest..."
# Initialize a Random Forest classifier with 100 trees
#forest = RandomForestClassifier(n_estimators=100)

# Fit the forest to the training set, using the bag of words as
# features and the sentiment labels as the response variable
#
# This may take a few minutes to run
#forest = forest.fit(train_data_features, train["sentiment"] )