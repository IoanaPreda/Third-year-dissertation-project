
close all; clear, clc

path= 'E:/Uni third\COMSOL - IP/code/20 sec/3 neurons 20 sec/2 freq 1000 um patch corner no delay 3 neurons/3 neurons surface selected/combined 3 neurons surface selected';
% path='E:/Uni third/COMSOL - IP/code/20 sec/1 neuron 20 sec/1 neuron 150 um corner patch/surface selected/combined surface selected.csv';
% path= "E:/Uni third/COMSOL - IP/code/20 sec/2 neurons 20 sec/2 freq 150 um patch corner no delay/surface selected/combined surface selected.csv";
% path= "E:\Uni third\COMSOL - IP\code\20 sec\2 neurons 20 sec\1 freq 150 um middle patch\surface selected\combined surface selected.csv";

%using the second file to represent the R matrix (first 100 sec of the signal)
path2='E:/Uni third/COMSOL - IP/code/20 sec/1 neuron 20 sec/1 neuron 150 um corner patch/surface selected/combined surface selected.csv';


name='V'; %parameter to use 
data = readtable(path);
data2= readtable(path2);
cols = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, name)& endsWith(data.Properties.VariableNames, '9E_4') );
cols2 = data2.Properties.VariableNames(startsWith(data2.Properties.VariableNames, name)& endsWith(data2.Properties.VariableNames, '13') );
cols_data = data{2:end, cols}; 
cols_data2= data2{2:end, cols2}; 

x = data(:,1:1); 
x= double(table2array(x)); %making this as index for time when plotting the truth wave

sz= size(cols_data); 
% zero_signal= zeros(sz);  %used for the first 100 seconds when no signal is present
data_b= [cols_data2;cols_data]; %create the mixure between the 2 signals having a total of 200 seconds otherwise only cols_data is used

% Create covariance matrices
Signal = data_b';

% compute covariance matrix R (first half of data)
part_data1 = Signal(:,1:1000);
part_data1 = bsxfun(@minus,part_data1,mean(part_data1,2));%--> taking every data point (i,j) and subtracting the mean from it (like 2 nested 'for' loops)
covR = part_data1*part_data1'/999; % divide by the number of samples in the matrix 

%used when only the original signal (cols_data) is decomposed
% part_data1 = bsxfun(@minus,part_data1,mean(part_data1,2));
% part_data1 = Signal(:,1:500); 
% covR = part_data1*part_data1'/499; 


%covariance matrix S (second half of data)
part_data2 = Signal(:,1001:end);
part_data2 = bsxfun(@minus,part_data2,mean(part_data2,2));
covS = part_data2*part_data2'/999;

%used when only the original signal (cols_data) is decomposed
% part_data2 = Signal(:,501:end);
% part_data2 = bsxfun(@minus,part_data2,mean(part_data2,2));
% covS = part_data2*part_data2'/499;

%plot the two covariance matrices
figure(2)
% S matrix
subplot(122)
imagesc(covS)
title('S matrix')
axis square
colorbar; hold on

% R matrix
subplot(121)
imagesc(covR)
title('R matrix')
axis square
colorbar;

% for S*inv(R)--> not needed now
% subplot(133)
% imagesc(inv(covR)*covS)
% title('R^-^1S matrix')
% axis square
% colorbar;


% Generalized eigendecomposition (GED)
[evecs,evals] = eig(covS, covR);
max_eval = 1e3;
min_eval= -1;

% avoid the instances when the eigenvalue reaches infinity
evals(evals > max_eval) = max_eval;
evals(evals < min_eval) = min_eval;

% sort eigenvalues/vectors
[evals,sidx] = sort(diag(evals),'descend'); %sidx represents the index for each value depending on the order from the highest to lowest
%making sure the eigenvalues are arranged in the right order so that thy can be plotted accordingly from largest to the smallest 
evecs = evecs(:,sidx); 

% plot the eigenspectrum
figure
subplot(221)
plot(evals./max(evals),'ks-','markersize',10,'markerfacecolor','m')
axis square
title('GED eigenvalues')
xlabel('Component number'), ylabel('Power ratio (\lambda)')

% raw signal plot
subplot(2,2,3:4)
plot(1:0.1:200.9,data_b, 'linewidth', 1.6)
% plot(1:0.1:100.9,data_b, 'linewidth', 1.6)
title('Original Signal')
xlabel('Time (s)')
if name=='V'
    ylabel('Electric Potential (V)')
else
    ylabel('Electric field (V/m)')
end
xlim([0 200]); %for 200 seconds
% xlim([0 100]); % for 100 seconds


% correlation plot between covariance matrices
subplot(322)
uu=corr(covR(:),covS(:)); %vectorize the matrices 
plot(covS(:),covR(:), 'mo')
title('R & S - Correlation')
