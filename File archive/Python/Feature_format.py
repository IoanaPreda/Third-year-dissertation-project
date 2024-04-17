import pandas as pd
import numpy as np
import os
# from scipy.fftpack import fft
from scipy.stats import kurtosis, skew


#calculating statistical features (only for normE)
def features_norm (df):
    norm= pd.DataFrame(df)
    rms_val=[]
    rms_name=[]

    kurt_name=[]
    kurt_val=[]

    skw_name=[]
    skw_val=[]

    std_name=[]
    std_val=[]

    for i in norm.columns:
        rms_name.append(i)
        kurt_name.append(i)
        skw_name.append(i)
        std_name.append(i)

    for i in range(len(df.columns)):
        a= np.sqrt(np.mean(np.square(norm.iloc[:,i])))
        rms_val.append(a)        

        kurt=kurtosis(norm.iloc[:,i], axis=0)
        kurt_val.append(kurt)

        skw=skew(norm.iloc[:,i], axis=0, bias=True)
        skw_val.append(skw)

        std= np.std(norm.iloc[:,i])
        std_val.append(std)


    return rms_val, rms_name, kurt_val, kurt_name, skw_val, skw_name, std_val, std_name

#calculating the total power and max power (only for potential)
def features_V (df):

    pow_name= []
    pow_val=[]

    fft_name=[]
    fft_val=[]

    pow_max=[]

    for i in df.columns:
        pow_name.append(i)
        fft_name.append(i)

    for i in range(len(df.columns)):
        ft=(np.fft.fft(df.iloc[:,i]-np.mean(df.iloc[:,i])))
        ft=np.abs(ft)
        fft_val.append(np.sum(ft[:int(1001/2)]))

        ft=ft.reshape(1,1001)
        pxx=ft[:int(1001/2)]**2
        for j in pxx:
            pow_val.append(np.sum(j))
        pow_max.append(np.max(pxx))

    return pow_val, pow_name, pow_max, fft_val, fft_name

#extracting all features from available files of simulations
def find_features(path):

    column=[]
    dff_norm=[]
    dff_V=[]

    for subdir, _, files in os.walk(path):
        for filename in files:
            if filename.startswith('comb'):
                df = pd.read_csv(os.path.join(subdir, filename))
                df= df.add_suffix(' '+ subdir[37:43])
                column = [col for col in df if 'NormE' in col ]
                dff_norm.append(df[column])
                column2= [col for col in df if 'V' in col]
                dff_V.append(df[column2])

    dfs_norm= pd.concat(dff_norm, axis=1)
    dfs_V= pd.concat(dff_V, axis=1)

####################################################################################
##excluding the files where the distance between sources is smaller than 100 um
    # for i in dfs_V.columns:
    #     # if '14' in i and not ('1 neur') in i:
    #     if '2 neur' in i:
    #         dfs_V= dfs_V.loc[:, ~dfs_V.columns.str.contains('14')]
    #     #    dfs_V= dfs_V.drop(i, axis=1)
    # for i in dfs_norm.columns:
    #     if '2 neur' in i:
    #         dfs_norm= dfs_norm.loc[:, ~dfs_norm.columns.str.contains('14')]
######################################################################################

    rms_val, rms_name, kurt_val, kurt_name, skw_val, skw_name, std_val, std_name= features_norm(dfs_norm)
    pow_val, pow_name, pow_max, fft_val, fft_name= features_V(dfs_V)


    return rms_val, rms_name, kurt_val, kurt_name, skw_val, skw_name, std_val, std_name, pow_val, pow_name, pow_max, fft_val, fft_name




