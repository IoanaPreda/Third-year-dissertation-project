close all; clear, clc

path= "E:\Uni third\COMSOL - IP\code\20 sec\2 neurons 20 sec\1 freq 150 um middle patch\surface selected\combined surface selected.csv";
% path='E:/Uni third/COMSOL - IP/code/20 sec/1 neuron 20 sec/1 neuron 150 um corner patch/surface selected/combined surface selected.csv';
% path= "E:/Uni third/COMSOL - IP/code/20 sec/2 neurons 20 sec/2 freq 150 um patch corner no delay/surface selected/combined surface selected.csv";
% path= "E:\Uni third\COMSOL - IP\code\20 sec\3 neurons 20 sec\2 freq 1000 um patch corner no delay 3 neurons\3 neurons surface selected\combined 3 neurons surface selected.csv";

%selecting the distance between source and the parameters of interest
data = readtable(path);
cols = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, 'es_Ez') & endsWith(data.Properties.VariableNames, '13'));
cols_data = data{:, cols};
cols2 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, 'es_Ex') & endsWith(data.Properties.VariableNames, '13'));
cols_data2 = data{:, cols2};

n=5; % first probe number
m=11; %second probe number

%plotting the data depeding on the parameter chosen including both probes

%first selected data
figure()
subplot(2,1,1)
plot (0:0.1:100,cols_data(:,n), 'linewidth', 1.6, 'DisplayName', strcat('probe ', num2str( n)));hold on;
plot(0:0.1:100, cols_data(:,m), 'linewidth', 1.6,'DisplayName',  strcat('probe ', num2str( m)))
title('Electric field in z direction')
legend('show')
xlabel('Time (s)')
ylabel ('Electric field (V/m)')

%second selected data
subplot(2,1,2)
plot (0:0.1:100,cols_data2(:,n), 'linewidth', 1.6, 'DisplayName', strcat('probe ', num2str( n)));hold on;
plot(0:0.1:100, cols_data2(:,m), 'linewidth', 1.6,'DisplayName',  strcat('probe ', num2str( m)))
title('Electric field in x direction')
legend('show')
xlabel('Time (s)')
ylabel ('Electric field (V/m)')

%doing the cross correlation between probes and plotting the results
[c,lag]=xcorr(cols_data(:,n), cols_data(:,m));
[c2,lag2]=xcorr(cols_data2(:,n), cols_data2(:,m));

figure()
plot(-100:0.1:100, c, 'linewidth', 1.6); hold on
plot(-100:0.1:100, c2, 'linewidth', 1.6)
legend ('Electric field in z', 'Electric field in x')
xlabel('Lag')
ylabel('Correlation')
title('Cross-Correlation')