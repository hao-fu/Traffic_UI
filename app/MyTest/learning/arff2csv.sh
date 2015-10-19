#java weka.core.converters.CSVSaver -i train_ui_pcap_ocsvm_all.arff -o train_ui_pcap_ocsvm_all.csv
#java weka.core.converters.CSVSaver -i test_ui_pcap_ocsvm_all.arff -o test_ui_pcap_ocsvm_all.csv
#java weka.core.converters.CSVSaver -i train_ui_pcap_ocsvm_all_few.arff -o train_ui_pcap_ocsvm_all_few.csv
#java weka.core.converters.CSVSaver -i train_ui_pcap_ocsvm_all_non_few.arff -o train_ui_pcap_ocsvm_all_non_few.csv
#java weka.core.converters.CSVSaver -i train_ui_pcap_ocsvm_all_non.arff -o train_ui_pcap_ocsvm_all_non.csv
#java weka.core.converters.CSVSaver -i poten_pcap_all.arff -o poten_pcap_all.csv
java weka.filters.unsupervised.attribute.Remove -R 1 -i train_ui_pcap_non_ocsvm_new.arff  -o train_ui_pcap_non_ocsvm_new_noid.arff
java weka.core.converters.CSVSaver -i train_ui_pcap_non_ocsvm_new_noid.arff -o train_ui_pcap_non_ocsvm_new.csv