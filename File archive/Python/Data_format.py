import pandas as pd
import numpy as np
import os

parent_folder= 'E:/Uni third/COMSOL - IP/code/20 sec/1 neuron 20 sec/1 neuron 150 um middle patch' #current folder with txt files exported from COMSOL

for subdir, _, files in os.walk(parent_folder):  #looks for all the subfolders in the parent directory
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(subdir, file) #joins the file to the folder fipath
            df = pd.read_csv(file_path, skiprows=14, header=None)
            csv_name = os.path.splitext(file)[0] + '.csv'
            csv_path = os.path.join(subdir, csv_name)
            df.to_csv(csv_path, mode='w')
            df2= df[1::28] 
            df2.reset_index(drop=True, inplace=True)
            #make the index go from 0 to 100 with step 0.1--> sample rate
            elem = np.arange(start=0, step=0.1, stop=100.1, dtype=float)
            #make the index go from 0 to 20 with step 0.02--> sample rate
            # elem = np.arange(start=0, step=0.02, stop=20.1, dtype=float)
            index = np.round(elem, decimals=2)
            df2 = df2.set_index(index)

            df3= df[3::28]
            df3.reset_index(drop=True, inplace=True)
            df3 = df3.set_index(index)

            df4= df[5::28]
            df4.reset_index(drop=True, inplace=True)
            df4 = df4.set_index(index)

            df5= df[7::28]
            df5.reset_index(drop=True, inplace=True)
            df5 = df5.set_index(index)

            df6= df[9::28]
            df6.reset_index(drop=True, inplace=True)
            df6 = df6.set_index(index)

            df13= df[11::28]
            df13.reset_index(drop=True, inplace=True)
            df13 = df13.set_index(index)
 
            df7= df[13::28]
            df7.reset_index(drop=True, inplace=True)
            df7 = df7.set_index(index)

            df8= df[15::28]
            df8.reset_index(drop=True, inplace=True)
            df8 = df8.set_index(index)

            df9= df[17::28]
            df9.reset_index(drop=True, inplace=True)
            df9 = df9.set_index(index)

            df10= df[19::28]
            df10.reset_index(drop=True, inplace=True)
            df10 = df10.set_index(index)

            df11= df[21::28]
            df11.reset_index(drop=True, inplace=True)
            df11 = df11.set_index(index)

            df14= df[23::28]
            df14.reset_index(drop=True, inplace=True)
            df14 = df14.set_index(index)

            df12= df[25::28]
            df12.reset_index(drop=True, inplace=True)
            df12 = df12.set_index(index)

            df15= df[27::28]
            df15.reset_index(drop=True, inplace=True)
            df15 = df15.set_index(index)


            dfs = [ df2, df3, df4, df5,df6,df13,df7,df8,df9,df10,df11,df14,df12, df15] #creating one dataframe with all parameters extracted from COMSOL
            dff = pd.concat(dfs, join='outer', axis=1)
            dff.columns=['normE', 'es.EX', 'es.EY', 'es.EZ','es.tEX','es.tEY', 'es.tEZ', 'es.Ex', 'es.Ey', 'es.Ez', 'es.tEx', 'es.tEy', 'es.tEz', 'V']
            dff.index.name= 'Time'
            dff.to_csv(csv_path, mode='w')
