close all; clear, clc

path= "E:\Uni third\COMSOL - IP\code\20 sec\2 neurons 20 sec\2 freq 150 um patch corner no delay\surface selected\combined surface selected.csv";
% path= "E:\Uni third\COMSOL - IP\code\20 sec\1 neuron 20 sec\1 neuron 150 um corner patch\surface selected\combined surface selected.csv";
% path= "E:\Uni third\COMSOL - IP\code\20 sec\2 neurons 20 sec\1 freq 150 um patch corner\surface selected\combined surface selected.csv";
% path= "E:\Uni third\COMSOL - IP\code\20 sec\3 neurons 20 sec\2 freq 1000 um patch corner no delay 3 neurons\3 neurons surface selected\combined 3 neurons surface selected.csv";

data = readtable(path);
cols = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, 'V') & endsWith(data.Properties.VariableNames, '14'));
cols_data = data{:, cols}; 

% for 100 seconds
time= 100; %total time in the data
L=length(cols_data); %length data
Ts=0.1; % sampling time
Fs = 1/Ts; %sampling frequency

%for 20 seconds
% time= 20; %total time in the data
% L=length(cols_data); %length data
% Ts=0.02; % sampling time
% Fs = 1/Ts; %sampling frequency


%x axis for plots
f_axis = Fs*(0:(L/2))/L;
t_axis=(0:L-1)*Ts;


%3D plot for the original signal with all probes
figure()
[X2,Y2] = meshgrid(1:1:16,t_axis);
plot3(X2,Y2, cols_data, 'LineWidth',1.3)
grid on
ylabel('Time (s)')
xlabel('probe number')
zlabel('Electric Potential (V)')
title('Mixed Signal at each probe')

%2D plot using all probes
figure
plot(Y2, cols_data)
legend show

%fft calculation
Y = fftshift(fft(cols_data-mean(cols_data), L)); %centering around 0
P1= abs(Y);
% power calculation
data_fft = Y(L/2:end,:);
psdx = abs(data_fft).^2;
freq = 0:Fs/L:Fs/2;  

%power spectrum 3D plot
figure;
[X1,Y1] = meshgrid(1:1:16,freq);
plot3(Y1,X1,psdx, 'LineWidth',1.3)
grid on
title('Periodogram Using FFT')
xlabel('Frequency (Hz)')
ylabel('Probe number')
zlabel('Power')
xlim([0 0.2]); %concentrating on the most important part of the plot
% legend show

%3D amplitude plot from fft
[X,Y] = meshgrid(1:1:16,f_axis);
figure
Z = P1(501:end,:); %using only the positive side of the spectrum
plot3(Y, X,Z, 'LineWidth',1.3)
title('Amplitude spectrum')
ylabel('Probe number')
xlabel('Frequency (Hz)')
zlabel('Ampltitude')
xlim([0 0.5]);
grid on
hold on

