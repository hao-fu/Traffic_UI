%clear
%clc
close all

figure 

train_csv =  csvread('train_ui_pcap_non_allFeature_truth.csv', 1);
%train_csv(find(train_csv(:, 1) > 2000), :) = [];
train_data = train_csv(:, 1: end - 1);

train_labels = train_csv(:, size(train_csv, 2));
[N D] = size(train_csv);
nonLocData = train_data(train_labels==0,:);
badLocData = train_data(train_labels==1,:);
goodLocData = train_data(train_labels==2,:);

feature = 24;
x = nonLocData(:, feature);

hold on
h=cdfplot(x);
set(h, 'color', 'r', 'LineWidth', 2, 'LineStyle', '-')
y = badLocData(:, feature);

h=cdfplot(y);
set(h,'color','g', 'LineWidth', 2, 'LineStyle', '-')
z = goodLocData(:, feature);

h=cdfplot(z);
set(h,'color','b', 'LineWidth', 2, 'LineStyle', '-')
legend('non-loc', 'Illegal','Legal','Location','southeast');
title('')
xlabel('Max length of downlink TCP packet (bytes)')
ylabel('CDF')
hold off

figure
feature = 17;
x = nonLocData(:, feature);

hold on
h=cdfplot(x);
set(h, 'color', 'r', 'LineWidth', 2, 'LineStyle', '-')
y = badLocData(:, feature);

h=cdfplot(y);
set(h,'color','g', 'LineWidth', 2, 'LineStyle', '-')
z = goodLocData(:, feature);

h=cdfplot(z);
set(h,'color','b', 'LineWidth', 2, 'LineStyle', '-')
legend('non-loc', 'Illegal','Legal','Location','southeast');
title('')
xlabel('Max length of uplink TCP packet (bytes)')
ylabel('CDF')
hold off

feature = 11;
x = nonLocData(:, feature);
figure
hold on
h=cdfplot(x);
set(h, 'color', 'r', 'LineWidth', 2, 'LineStyle', '-')
y = badLocData(:, feature);

h=cdfplot(y);
set(h,'color','g', 'LineWidth', 2, 'LineStyle', '-')
z = goodLocData(:, feature);

h=cdfplot(z);
set(h,'color','b', 'LineWidth', 2, 'LineStyle', '-')
legend('non-loc', 'Illegal','Legal','Location','southeast');
title('')
xlabel('avg length of interval (ms)')
ylabel('CDF')
hold off


figure
feature = 4;
x = nonLocData(:, feature);

hold on
h=cdfplot(x);
set(h, 'color', 'r', 'LineWidth', 2, 'LineStyle', '-')
y = badLocData(:, feature);

h=cdfplot(y);
set(h,'color','g', 'LineWidth', 2, 'LineStyle', '-')
z = goodLocData(:, feature);

h=cdfplot(z);
set(h,'color','b', 'LineWidth', 2, 'LineStyle', '-')
legend('non-loc', 'Illegal','Legal','Location','southeast');
title('')
xlabel('mean length of total TCP packet (bytes)')
ylabel('CDF')
hold off


figure
feature = 1;
x = nonLocData(:, feature);

hold on
h=cdfplot(x);
set(h, 'color', 'r', 'LineWidth', 2, 'LineStyle', '-')
y = badLocData(:, feature);

h=cdfplot(y);
set(h,'color','g', 'LineWidth', 2, 'LineStyle', '-')
z = goodLocData(:, feature);

h=cdfplot(z);
set(h,'color','b', 'LineWidth', 2, 'LineStyle', '-')
legend('non-loc', 'Illegal','Legal','Location','southeast');
title('')
xlabel('frame num TCP packet (bytes)')
ylabel('CDF')
hold off