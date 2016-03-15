clear
clc
close all

% addpath to the libsvm toolbox
addpath('/home/hao/Downloads/libsvm-3.20/matlab');

% addpath to the data
%dirData = '/home/hao/Downloads/libsvm-3.20/matlab';
%addpath(dirData);

train_csv =  csvread('train_ui_pcap_ocsvm.csv', 1);
train_labels = train_csv(:, size(train_csv, 2));
train_features = train_csv(:, 1: end - 1);
train_features_sparese = sparse(train_features);
libsvmwrite('train_ocsvm.svm', train_labels, train_features_sparese)

test_csv =  csvread('test_ui_pcap_ocsvm.csv', 1);
test_labels = test_csv(:, size(test_csv, 2));
test_features = test_csv(:, 1: end - 1);
test_features_sparese = sparse(test_features);
libsvmwrite('test_ocsvm.svm', test_labels, test_features_sparese)

% read the data set
[train_label, train_inst] = libsvmread(fullfile('.','train_ocsvm.svm'));
[N D] = size(train_inst);

% Determine the train and test index: cross-validation
cut_point = ceil(N * 0.66);
trainIndex = zeros(N, 1); trainIndex(1: cut_point) = 1; % first cut_point number as training samples
crosstestIndex = zeros(N, 1); crosstestIndex(cut_point + 1:N) = 1;
trainData = train_inst(trainIndex==1,:);
for i = 1: D
    trainData(:, i) = scaledata(trainData(:, i), -1, 1);
end
trainLabel = train_label(trainIndex==1,:);
crosstestData = train_inst(crosstestIndex==1,:);
for i = 1: D
    crosstestData(:, i) = scaledata(crosstestData(:, i), -1, 1);
end
crosstestLabel = train_label(crosstestIndex==1,:);

% Train the SVM
% %trainLabel = ones(cut_point, 1);
model = svmtrain(trainLabel, trainData, '-s 2 -t 2 -n 0.05');
% Use the SVM model to classify the cross-validation
[cross_predicted_label] = svmpredict(crosstestLabel, crosstestData, model); % run the SVM model on the test data

[test_label, test_inst] = libsvmread(fullfile('.','test_ocsvm.svm'));
testData = test_inst;
[N_test, D] = size(test_inst);
testLabel = ones(N_test, 1);
for i = 1: D
    testData(:, i) = scaledata(testData(:, i), -1, 1);
end
[predicted_label] = svmpredict(testLabel, testData, model);


[c,g] = meshgrid(-10:0.1:10,-10:0.01:10);  
[m,n] = size(c);  
cg = zeros(m,n);  
eps = 10^(-4);  
v = 10;  
bestc = 1;  
bestg = 0.1;  
bestacc = 0; 
decCounter = 0;
counter = 0;
for i = 1:m
    if decCounter > 100 || counter > 500
        break
    end
    for j = n:n  
        counter = counter + 1;
        if decCounter > 100 || counter > 500
            break
        end
        cmd = ['-v ',num2str(v),' -t 2',' -c ',num2str(2^c(i,j)),' -g ',num2str(2^g(i,j)),' -s 2', ' -n 0.3'];  
        cg(i,j) = svmtrain(trainLabel,trainData,cmd);       
        if cg(i,j) > bestacc 
            fprintf('%f, %f\n', cg(i, j), bestacc)
            fprintf('%d\n', decCounter)
            bestacc = cg(i,j);  
            bestc = 2^c(i,j);  
            bestg = 2^g(i,j); 
            decCounter = -1;
        end          
%         if abs( cg(i,j)-bestacc )<=eps && bestc > 2^c(i,j)   
%             bestacc = cg(i,j);  
%             bestc = 2^c(i,j);  
%             bestg = 2^g(i,j);  
%             decCounter = -1; 
%         end  
        
        if decCounter ~= -1
            decCounter = decCounter + 1;
        else 
            decCounter = 0;
        end
        
    end  
end  
cmd = [' -t 2',' -c ',num2str(bestc),' -g ',num2str(bestg),' -n 0.3',' -s 2'];  
model = svmtrain(trainLabel, trainData, cmd);
[cross_predicted_label] = svmpredict(crosstestLabel, crosstestData, model);
[predicted_label] = svmpredict(testLabel, testData, model);

