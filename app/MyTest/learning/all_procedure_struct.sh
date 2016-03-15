#!/usr/bin/env bash
#python bag_of_words.py
#java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.bayes.NaiveBayes -t ~/Dropbox/workspace/app/app/MyTest/learning/train_UI.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/UI_predict_NB.out
#java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.functions.Logistic -t ~/Dropbox/workspace/app/app/MyTest/learning/train_UI.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/UI_predict_LG.out
##java -Xmx3000m weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.bayes.BayesNet -t ~/Dropbox/workspace/app/app/MyTest/learning/train_UI.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/UI_predict_NB.out
#java -Xmx2048m weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.trees.RandomForest -t ~/Dropbox/workspace/app/app/MyTest/learning/train_UI.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/UI_predict_RF.out
#python UI_out_voting.py
##python ui_pcap_feature_all.py
#python ui_pcap_nonloc_all.py
##java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.trees.RandomForest -t ~/Dropbox/workspace/app/app/MyTest/learning/train_ui_pcap_allFeature.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/ui_pcap.out
java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.trees.RandomForest -t ~/Dropbox/workspace/app/app/MyTest/learning/train_ui_pcap_non_allFeature_struct.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/ui_pcap_struct.out
##java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.trees.RandomForest -t ~/Dropbox/workspace/app/app/MyTest/learning/train_ui_pcap_non_allFeature.arff -T ~/Dropbox/workspace/app/app/MyTest/learning/test_ui_pcap__bad.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/test_bad.out
python TP_ground_struct.py