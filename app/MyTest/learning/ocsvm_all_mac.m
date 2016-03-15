clear
clc
close all

% addpath to the libsvm toolbox
%addpath('/Users/Hao/Downloads/libsvm-3.20/matlab');
% 
train_csv =  csvread('train_ui_pcap_ocsvm_all.csv', 1);
train_labels = train_csv(:, size(train_csv, 2));
train_features = train_csv(:, 1: end - 1);
train_features_sparese = sparse(train_features);
libsvmwrite('all_ocsvm.svm', train_labels, train_features_sparese)

% read the data set
[train_label, train_inst] = libsvmread(fullfile('.','all_ocsvm.svm'));
[N D] = size(train_inst);

% Determine the train and test index: cross-validation
%cut_point = ceil(N * 0.66);
cut_point = 1609;
trainIndex = zeros(N, 1); trainIndex(1: cut_point) = 1; % first cut_point number as training samples
testIndex = zeros(N, 1); testIndex(cut_point + 1:N) = 1;
trainData = train_inst(trainIndex==1,:);
numF = 24;
for i = 1: numF
    trainData(:, i) = scaledata(trainData(:, i), -1, 1);
end
trainLabel = train_label(trainIndex==1,:);
trainLabel = ones(size(trainData, 1), 1);
testData = train_inst(testIndex==1,:);
for i = 1: numF
    testData(:, i) = scaledata(testData(:, i), -1, 1);
end
testLabel = train_label(testIndex==1,:);
testLabel = zeros(size(testData, 1), 1);
testLabel(:, 1) = -1;
libsvmwrite('train_ocsvm.svm', trainLabel, trainData)
libsvmwrite('test_ocsvm.svm', testLabel, testData)

% Train the SVM
% %trainLabel = ones(cut_point, 1);
cmd = ['-t 2  -s 2', ' -n 0.01'];  
model = svmtrain(trainLabel, trainData, cmd);
% Use the SVM model to classify the test data
[predicted_label] = svmpredict(testLabel, testData, model);
cmd = ['-v 10 -t 2  -s 2', ' -n 0.01'];  
model = svmtrain(trainLabel, trainData, cmd);

[c,g] = meshgrid(-100: 1:100, -100: 1: 100);  
%c = transpose(c);
[m, n] = size(c);  
cg = zeros(m,n);  
eps = 10^(-4);  
v = 10;  
bestc = 1;  
bestg = 0.1;  
bestacc = 0; 
decCounter = 0;
counter = 0;
result = [0 0 0 0 0];
for i = 1:m
%     if %decCounter > 100000 %|| counter > 50000000
%         break
%     end
    
    for j = n:n 
%         counter = counter + 1;
%         if decCounter > 100000 %|| counter > 500
%             break
%         end
        cmd = ['-v ',num2str(v),' -t 2',' -c ',num2str(2^c(i,j)),' -g ',num2str(2^g(i, j)),' -s 2', ' -n 0.15'];  
        cg(i,j) = svmtrain(trainLabel,trainData,cmd);       
        if cg(i,j) > bestacc 
            fprintf('%f, %f\n', cg(i, j), bestacc)
            fprintf('%d\n', decCounter)
            bestacc = cg(i,j);  
            bestcc = 2^c(i,j);  
            bestcoo = c(i, j);
            bestgg = 2^g(i,j);
            bestgoo = g(i, j);
            %decCounter = -1;
        end          
%         if abs( cg(i,j)-bestacc )<=eps && bestc > 2^c(i,j)   
%             bestacc = cg(i,j);  
%             bestc = 2^c(i,j);  
%             bestg = 2^g(i,j);  
%             decCounter = -1; 
%         end  
        cmd = [' -t 2',' -c ',num2str(2^c(i,j)),' -g ',num2str(2^g(i, j)),' -n 0.15',' -s 2'];  
        model = svmtrain(trainLabel, trainData, cmd);
        [predicted_label, accuracy, a] = svmpredict(testLabel, testData, model);
        result =  [result; accuracy(1) cg(i, j) accuracy(1)+cg(i, j) c(i,j) g(i, j)];
        accuracy(1)+cg(i, j)
%         if decCounter ~= -1
%             decCounter = decCounter + 1;
%         else 
%             decCounter = 0;
%         end
        if accuracy(1) > 80 
            if cg(i, j) > 80
               fprintf( 'hahahahhaha')
            bestc = 2^c(i,j);
            bestg = 2^g(i,j);
            %break
            end
        end
        fprintf( '%f', accuracy(1))
        
    end  
%     if accuracy(1) > 80 
%         if cg(i, j) > 80
%             break
%         end
%     end
end  

cmd1 = ['-v 10 -t 2',' -c ',num2str(bestc),' -g ',num2str(bestg),' -n 0.15',' -s 2'];  
svmtrain(trainLabel, trainData, cmd1);
cmd = [' -t 2',' -c ',num2str(bestc),' -g ',num2str(bestg),' -n 0.15',' -s 2'];  
model = svmtrain(trainLabel, trainData, cmd);
[predicted_label, accracy, a] = svmpredict(testLabel, testData, model);
