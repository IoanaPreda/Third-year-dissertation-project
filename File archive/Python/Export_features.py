import Feature_format
import pandas as pd

path= 'E:/Uni third/COMSOL - IP/code/20 sec' #folder with all the simulation data

source_name=[]
source_val=[]
rms_name2=[]

rms_val, rms_name, kurt_m, kurt_name, skw_m, skw_name, std_val, std_name, pow_m, pow_name, pow_max, fft_m, fft_name=Feature_format.find_features(path)

for elem in rms_name:
    rms_name2.append(elem.replace('NormE ', ''))  #correcting the name for each data entry

#adding the classes
for i in rms_name:
    if '3 neur'in i:
        source_name= ['source no']
        source_val.append('3')
    if '2 neur' in i:
        source_name= ['source no']
        source_val.append ('2')
    elif '1 neur' in i:
        source_name= ['source no']
        source_val.append('1')


dfFeatures =  pd.DataFrame({'Names': rms_name2,'RMS': rms_val, 'KURT': kurt_m, 'SKW': skw_m,'STD': std_val, 'POW': pow_m, 'POW_Max': pow_max, 'FFT': fft_m, 'Sources': source_val})
dfFeatures.to_csv('20 sec\Train_data-50--above.csv')#exporting all features
print(dfFeatures['Sources'].value_counts()) #the number of samples for each class

