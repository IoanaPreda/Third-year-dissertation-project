close all; clear, clc
path= "E:/Uni third/COMSOL - IP/code/20 sec/2 neurons 20 sec/2 freq 150 um patch corner no delay/surface selected/probe5_p_0.0013.csv";
% path='E:/Uni third/COMSOL - IP/code/20 sec/1 neuron 20 sec/1 neuron 150 um corner patch/surface selected/probe5_p_0.0013.csv';
% path= "E:/Uni third/COMSOL - IP/code/20 sec/2 neurons 20 sec/2 freq 150 um patch corner no delay/surface selected/probe5_p_0.0013.csv";
% path= "E:\Uni third\COMSOL - IP\code\20 sec\3 neurons 20 sec\2 freq 1000 um patch corner no delay 3 neurons\3 neurons surface selected\probe5_p_9E-4.csv";


data = readtable(path);
cols = data.Properties.VariableNames(startsWith(data.Properties.VariableNames, 'V'));
cols_data = data{:, cols};
x = data(:,1:1); %index column for sample time
x= double(table2array(x));


emd(cols_data,'Display',1); %emd information for each imf (also includes the default plot)
[imf, res]=emd(cols_data); 

%plotting the imfs to match the model used in Python
figure
subplot (size(imf,2)+2,1,1)
plot(x,cols_data,'r', 'LineWidth', 1.6)
title('Original Signal');
for i=1:size(imf,2)
    subplot(size(imf,2)+2,1,i+1);
    txt=['IMF ',num2str(i)];
    plot(x,imf(:,i), 'LineWidth', 1.6);
    title (txt)
    hold on;
end
subplot(size(imf,2)+2, 1, size(imf,2)+2)
plot(x, res,'Color',[0, 0.6, 0], 'LineWidth',1.6)
title('Residue');
xlabel('Time (s)');

%instantaneous frequency plot
figure
for i= 1:size(imf,2)
IF=instfreq(imf(:,i),10,'Method','hilbert');
plot(x(1:1000),IF, 'linewidth', 1.6); hold on
legend('IMF1', 'IMF2', 'IMF3', 'IMF4');
    ylabel('Frequency (Hz)')
    xlabel('Time (s)')
%     xlim([0 0.3])
    title('Instantaneous Frequency')
end

%pmsi calculation
m=2; %decides which imfs to consider
num= sum(imf(:,m).^2)+sum(imf(:,m+1).^2);
pmsi= max(abs(dot(imf(:,m), imf(:,m+1), 1))/num,0)
