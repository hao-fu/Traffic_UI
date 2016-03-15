#!/usr/bin/env bash
#java weka.classifiers.trees.RandomForest  weka.filters.unsupervised.attribute.Remove -R 1 -T ~/Dropbox/workspace/app/app/MyTest/learning/poten_pcap_all.arff -l ~/Dropbox/workspace/app/app/MyTest/learning/rf_3class.model -p 1 > ~/Dropbox/workspace/app/app/MyTest/learning/poten_feat.out
##java weka.filters.unsupervised.attribute.AddID -i ~/Dropbox/workspace/app/app/MyTest/learning/train_ui_pcap_ocsvm_all_non.arff -o ~/Dropbox/workspace/app/app/MyTest/learning/train_ui_pcap_ocsvm_all_non_id.arff
#java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.trees.RandomForest -t ~/Dropbox/workspace/app/app/MyTest/learning/train_ui_pcap_ocsvm_all_non_id.arff -T ~/Dropbox/workspace/app/app/MyTest/learning/poten_pcap_all.arff -p 1 > ~/Dropbox/workspace/app/app/MyTest/learning/poten_feat.out
java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.trees.RandomForest -t ~/Dropbox/workspace/app/app/MyTest/learning/train_ui_pcap_non_allFeature_truth.arff -T ~/Dropbox/workspace/app/app/MyTest/learning/poten_pcap_all.arff -p 1 > ~/Dropbox/workspace/app/app/MyTest/learning/poten_feat.out


