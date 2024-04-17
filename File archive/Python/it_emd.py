import matplotlib.pyplot as plt
import numpy as np
import emd
import pandas as pd
from it_emd_function import it_emd #importing the function for iterated masking emd


folder_path= "E:/Uni third/COMSOL - IP/code/20 sec/2 neurons 20 sec/2 freq 150 um patch middle/surface selected/probe5_p_0.0013.csv"

df = pd.read_csv(folder_path)
column = df['V'].values
column = df['normE'].values #chossing between normE or potential (V)
x=df.iloc[:, 0].values #sampling time
dfs=pd.DataFrame(column)

plt.rc('font', size=10)
np.random.seed(6) 
Fs = 10 #sampling frequency
n=3 # number of imfs to allow for masking signal calculation
m0 = np.random.randint(1, 128, size=n) / Fs #first mask generation as part of it_emd

nit, m_all, imfs, mask_eq, mask_std, imf_all = it_emd(column, N_imf=n, N_iter_max=15, N_avg=1, sample_rate=Fs, verbose=True, mask_0=m0, iter_th=0.01, w_method='power')

im= emd.sift.sift(column) #to be able to plot the residue since the it_emd does not provide this feature
imf2=imfs.transpose()
# plt.figure()
for i, imf in enumerate(imf2):
    plt.subplot(len(imf2)+2, 1, i+2)
    plt.plot(x, imf)
    plt.title("IMF %d" % (i+1), fontsize=10, fontweight='bold')
plt.subplot(len(imf2)+2, 1, 1)
plt.plot(x,column, 'r')
plt.title("Original signal", fontsize=13, fontweight='bold')
plt.subplot(len(imf2)+2, 1, len(imf2)+2)
plt.plot(x,np.ravel(im[:,-1:]), 'g')
plt.title("Residue", fontsize=10, fontweight='bold')
plt.xlabel('Time (s) ')
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
plt.show()


#PMSI
m=0
num= sum(imfs[:, m]**2) + sum(imfs[:, m+1]**2)
pmsi2 = np.max([abs(np.dot(imfs[:, m], imfs[:,m+1])) / num, 0])
print(pmsi2)

#instantaneous frequency plot for all imfs
IP, IF, IA = emd.spectra.frequency_transform(imfs, 10, 'hilbert')
fig, axs = plt.subplots(nrows=1, ncols=1)
axs.plot(x,IF)
axs.set_title('Instantaneous Frequency')
plt.legend(['IMF1', 'IMF2', 'IMF3'])
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.tight_layout()
plt.show ()
