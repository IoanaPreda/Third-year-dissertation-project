close all; clear, clc
path= 'E:\Uni third\COMSOL - IP\code\20 sec\1 neuron 20 sec\x direction sweep\z=1.2\combined z=1.2.csv';  %data at each probe from one source
path0="E:\Uni third\COMSOL - IP\code\neuron data\probe4_q_0.001.csv"; %data for ground truth of one source

path3= "E:\Uni third\COMSOL - IP\code\20 sec\2 neurons 20 sec\2 freq 150 um patch corner no delay\surface selected\combined surface selected.csv"; %testing data
% path3= 'E:/Uni third\COMSOL - IP/code/20 sec/3 neurons 20 sec/2 freq 1000 um patch corner no delay 3 neurons/3 neurons surface selected/combined 3 neurons surface selected.csv';
% path3= "E:\Uni third\COMSOL - IP\code\20 sec\1 neuron 20 sec\x direction sweep\z=1.2\combined z=1.2.csv";

data00 = readtable(path3);
cols00 = data00.Properties.VariableNames(startsWith(data00.Properties.VariableNames, 'V')& endsWith(data00.Properties.VariableNames, '11'));
cols_data00 = data00{:, cols00};

param= 'V';

data0 = readtable(path0);
cols0 = data0.Properties.VariableNames(startsWith(data0.Properties.VariableNames, 'V'));
cols_data0 = data0{:, cols0};

data = readtable(path);

%obtaining data for each probe at all 16 positions
cols = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '01'));
cols_data = data{:, cols};

cols2= data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '11'));
cols_data2 = data{:, cols2};

cols3 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '12'));
cols_data3 = data{:, cols3};

cols4 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '13'));
cols_data4 = data{:, cols4};

cols5 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '14'));
cols_data5 = data{:, cols5};

cols6 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '15'));
cols_data6 = data{:, cols6};

cols7 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '16'));
cols_data7 = data{:, cols7};

cols8 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '17'));
cols_data8 = data{:, cols8};

cols9 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '18'));
cols_data9 = data{:, cols9};

cols10 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '19'));
cols_data10 = data{:, cols10};

cols11 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '02'));
cols_data11 = data{:, cols11};

cols12 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '021'));
cols_data12 = data{:, cols12};

cols13 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '022'));
cols_data13 = data{:, cols13};

cols14 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '023'));
cols_data14 = data{:, cols14};

cols15 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '024'));
cols_data15 = data{:, cols15};

cols16 = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, param) & endsWith(data.Properties.VariableNames, '025'));
cols_data16 = data{:, cols16};


time= 20; %total time in the data
L=length(cols_data);
L0= length(cols_data0); %length data
Ts=0.02; % sampling time
Fs = 1/Ts; %sampling frequency
freq = 0:Fs/L:Fs/2; 

%ground truth power
Y0 = fftshift(fft(cols_data0, L0));
data_fft0 = Y0(L/2:end,:);
psdx0 = abs(data_fft0).^2;
tot_pow0= (sum(psdx0)); 
signal= tot_pow0.*eye(16);

%test signal power to identify the number of sources
for i=1:size(cols_data00,2)
Y00 = fftshift(fft(cols_data00(:,i), L0));
data_fft00 = Y00(L/2:end,:);
psdx00 = abs(data_fft00).^2;
tot_pow00= (sum(psdx00)); 
pos00(i,:)=tot_pow00;
end


%finding the power at each probe for each position to create matrix A
for i=1:size(cols_data,2)
Y = fftshift(fft(cols_data(:,i), L));
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
tot_pow= (sum(psdx));
pos(i,:)=tot_pow;
end

for i=1:size(cols_data2,2)
Y = fftshift(fft(cols_data2(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
tot_pow= (sum(psdx));
pos1(i,:)=tot_pow;
end

for i=1:size(cols_data3,2)
Y = fftshift(fft(cols_data3(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
% max_pow= max(psdx);
tot_pow= (sum(psdx));
% max_pow=trapz(freq, psdx); 
pos2(i,:)=tot_pow;
end

for i=1:size(cols_data4,2)
Y = fftshift(fft(cols_data4(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
% max_pow= max(psdx);
tot_pow= (sum(psdx));
% max_pow=trapz(freq, psdx); 
pos3(i,:)=tot_pow;
end

for i=1:size(cols_data5,2)
Y = fftshift(fft(cols_data5(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
% max_pow= max(psdx);
tot_pow= (sum(psdx));
% max_pow=trapz(freq, psdx); 
pos4(i,:)=tot_pow;
end

for i=1:size(cols_data6,2)
Y = fftshift(fft(cols_data6(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
tot_pow= (sum(psdx));
pos5(i,:)=tot_pow;
end

for i=1:size(cols_data7,2)
Y = fftshift(fft(cols_data7(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
tot_pow= (sum(psdx));
pos6(i,:)=tot_pow;
end

for i=1:size(cols_data8,2)
Y = fftshift(fft(cols_data8(:,i), L));
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
tot_pow= (sum(psdx));
pos7(i,:)=tot_pow;
end

for i=1:size(cols_data9,2)
Y = fftshift(fft(cols_data9(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
tot_pow= (sum(psdx));
pos8(i,:)=tot_pow;
end

for i=1:size(cols_data10,2)
Y = fftshift(fft(cols_data10(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
tot_pow= (sum(psdx));
pos9(i,:)=tot_pow;
end

for i=1:size(cols_data11,2)
Y = fftshift(fft(cols_data11(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
tot_pow= (sum(psdx));
pos10(i,:)=tot_pow;
end

for i=1:size(cols_data12,2)
Y = fftshift(fft(cols_data12(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
tot_pow= (sum(psdx));
pos11(i,:)=tot_pow;
end

for i=1:size(cols_data13,2)
Y = fftshift(fft(cols_data13(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
tot_pow= (sum(psdx));
pos12(i,:)=tot_pow;
end

for i=1:size(cols_data14,2)
Y = fftshift(fft(cols_data14(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
tot_pow= (sum(psdx));
pos13(i,:)=tot_pow;
end

for i=1:size(cols_data15,2)
Y = fftshift(fft(cols_data15(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
tot_pow= (sum(psdx));
pos14(i,:)=tot_pow;
end

for i=1:size(cols_data16,2)
Y = fftshift(fft(cols_data16(:,i), L));
% power
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
tot_pow= (sum(psdx));
pos15(i,:)=tot_pow;
end

%finding the coefficients based on the power components and ground truth
a= pos.*diag(inv(signal));
a1= pos1.* diag(inv(signal));
a2= pos2.* diag(inv(signal));
a3= pos3.* diag(inv(signal));
a4= pos4.* diag(inv(signal));
a5= pos5.* diag(inv(signal));
a6= pos6.* diag(inv(signal));
a7= pos7.* diag(inv(signal));
a8= pos8.* diag(inv(signal));
a9= pos9.* diag(inv(signal));
a10= pos10.* diag(inv(signal));
a11= pos11.* diag(inv(signal));
a12= pos12.* diag(inv(signal));
a13= pos13.* diag(inv(signal));
a14= pos14.* diag(inv(signal));
a15= pos15.* diag(inv(signal));

A=[a,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15];
A_= inv(A);

rev= A_(:,2).*pos00; %obtaining the most important components for the test signal

%plotting the components
figure
stem(1:1:16, abs(rev), 'linewidth', 1.6)
xlabel('Component number')
ylabel ('Component Intensity')




