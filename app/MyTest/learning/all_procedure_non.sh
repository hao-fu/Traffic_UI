#python bag_of_words.py
#java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.bayes.NaiveBayes -t ~/Dropbox/workspace/app/app/MyTest/learning/train_UI.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/UI_predict_NB.out
##java -Xmx3000m weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.bayes.BayesNet -t ~/Dropbox/workspace/app/app/MyTest/learning/train_UI.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/UI_predict_NB.out
#java -Xmx2048m weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.trees.RandomForest -t ~/Dropbox/workspace/app/app/MyTest/learning/train_UI.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/UI_predict_RF.out
#python UI_out_voting.py
python ui_pcap_nonloc_all.py
java weka.classifiers.meta.FilteredClassifier -F weka.filters.unsupervised.attribute.RemoveType -W weka.classifiers.trees.RandomForest -t ~/Dropbox/workspace/app/app/MyTest/learning/train_ui_pcap_non_allFeature.arff -p 1 -i > ~/Dropbox/workspace/app/app/MyTest/learning/ui_pcap_non.out
python TP_ground_non.py