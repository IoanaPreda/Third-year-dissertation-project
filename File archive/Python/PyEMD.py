import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from PyEMD import EMD
import emd


folder_path= 'E:/Uni third\COMSOL - IP/code/20 sec/3 neurons 20 sec/2 freq 1000 um patch corner no delay 3 neurons/3 neurons surface selected'

for subdir, _, files in os.walk(folder_path):
        for filename in files:
            if filename.startswith('probe5_') and filename.endswith('13.csv'): #choosing the probe and the distance between sources
                df = pd.read_csv(os.path.join(subdir, filename))
                column = df['V'].values
                #column = df['normE'].values #chossing between normE or potential (V)
                x=df.iloc[:, 0].values # sampling time 
                emd1 = EMD()
                imfs = emd1.emd(column,x)
                # upper_env = emd.sift.interp_envelope(column, mode='upper')
                # lower_env = emd.sift.interp_envelope(column, mode='lower')
                # avg_env = (upper_env+lower_env) / 2

#         Plot the IMFs and the original signal
                plt.figure()
                for i, imf in enumerate(imfs): # used to loop over a list but also keep track of the current iteration
                    plt.subplot(len(imfs)+1, 1, i+2)  
                    plt.plot(x, imf)
                    plt.title("IMF %d" % (i+1), fontweight='bold') 
                    if i == len(imfs) -1:
                        plt.title("Residue", fontweight='bold')
                        plt.plot(x, imf, 'g')
                        plt.xlabel('Time (s)')
                    plt.subplot(len(imfs)+1, 1, 1)
                    plt.plot(x,column, 'r') 
                    # plt.plot(x, avg_env, 'r')
                    # plt.plot(x, upper_env, 'g')
                    # plt.plot(x, lower_env, 'tab:orange')
                    plt.title("Original signal", fontweight='bold')
                    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
plt.show()

#instantaneous frequency plot for imfs
Fs=10 #sampling frequency
imf=imfs.transpose()
IP, IF, IA = emd.spectra.frequency_transform(imf[:,:-1], Fs, 'hilbert')
fig, axs = plt.subplots(nrows=1, ncols=1)
axs.plot(x, IF)
axs.set_title('Instantaneous Frequency')
plt.legend(['IMF1', 'IMF2', 'IMF3'])
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.tight_layout()
plt.show ()

#pmsi value for consecutive pairs of imfs
m=0
num= sum(imfs[m, :]**2) + sum(imfs[m+1, :]**2)
pmsi2 = np.max([abs(np.dot(imfs[m,:], imfs[m+1,:])) / num, 0])
print(pmsi2)