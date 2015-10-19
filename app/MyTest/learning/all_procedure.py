__author__ = 'hao'

import os

os.popen('python bag_of_words.py')
os.popen('java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.bayes.NaiveBayes -t'
         ' ~/Dropbox/workspace/app/app/MyTest/train_UI.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/UI_predict_NB.out')
os.popen('java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W  weka.classifiers.trees.RandomForest -t'
         ' ~/Dropbox/workspace/app/app/MyTest/train_UI.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/UI_predict_RF.out')
os.popen('python ui_out_voting.py')
os.popen('python ui_pcap_feature_all.py')
os.popen('java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.trees.RandomForest -t'
         ' ~/Dropbox/workspace/app/app/MyTest/learning/train_ui_pcap_allFeature.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/ui_pcap.out')
os.popen('python TP_ground.py')