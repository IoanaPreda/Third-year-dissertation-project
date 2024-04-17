import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

path= 'E:/Uni third/COMSOL - IP/code/20 sec/Train_data-50--2.csv'

df = pd.read_csv(path)
data= df.iloc[:,2:-2] #--> x
# data= df[['SKW','POW']]
# data= pd.DataFrame(scaler.fit_transform(data))
task = df['Sources']#-->y

#target class information
print(df['Sources'].value_counts())
print(df['Sources'].value_counts()/float(len(df)))

#splitting data for training and testing
x_train, x_test, y_train, y_test = train_test_split(data, task, test_size = 0.2, shuffle=True)

#feature scaling
scaler= MinMaxScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)
x_train = pd.DataFrame(x_train)
x_test = pd.DataFrame(x_test)

# for 2 sources gamma=C-->0.1 for 3 source C=100 and gamma=1
#classifier 
C=100
gamma=1
svc2= SVC(C=C, gamma=gamma)

# fitting the classifier according to the training data
svc2.fit(x_train,y_train)

# use the train data to make preditions
y_pred=svc2.predict(x_test)

#Accuracy infromation
print('Accuracy: {0:0.2f}%'. format(accuracy_score(y_test, y_pred)*100))
print('Training accuracy: {:.2f}%'.format(svc2.score(x_train, y_train)*100))
print(classification_report(y_test, y_pred)) #--> check for precision, f1-score and support 

#confusion matrix for 3 sources
cm = confusion_matrix(y_test, y_pred)
cm_matrix = pd.DataFrame(data=cm, columns=['Pred 1 source', 'Pred 2 sources','Pred 3 sources' ], 
                                 index=['Actual 1 source', 'Actual 2 sources', 'Actual 3 sources'])
sns.heatmap(cm_matrix, annot=True, fmt='d', cmap='YlGnBu')
plt.tight_layout()
plt.show()

#confusion matrix for 2 sources
# cm = confusion_matrix(y_test, y_pred)
# cm_matrix = pd.DataFrame(data=cm, columns=['Pred 1 source', 'Pred 2 sources' ], 
#                                  index=['Actual 1 source', 'Actual 2 sources'])
# sns.set(font_scale=1.2)
# sns.heatmap(cm_matrix, annot=True, fmt='d', cmap='YlGnBu')
# plt.tight_layout()
# plt.show()

################ Feature distribution plot ##############################
# for i, col in enumerate (data):
#     plt.subplot(2,3,i+1)
#     plt.scatter( task, data.iloc[:,i], c= task)  
#     plt.ylabel(col) 
#     plt.xlabel('Number of sources')
#     plt.xticks([1,2,3])
#     plt.tight_layout()
# plt.show()

# sns.pairplot(df.iloc[:,1:],hue='Sources')
# plt.tight_layout()
# plt.show()
########################################################################


#10 fold validation scores and plot
kfold=KFold(n_splits=10, shuffle=True, random_state=0)
scores = cross_val_score(svc2, x_train, y_train, cv=kfold)
print('10-fold validation scores:\n{}'.format(scores))
print('Average cross-validatio score {}%'.format(np.mean(scores*100)))
x= np.arange(1,11,1)
plt.plot(x,scores*100, marker='o')
plt.ylabel('Accuracy score (%)')
plt.xlabel("Fold number")
plt.show()


####################### GRID SEARCH ##################################

parameters= {'C': [0.01,0.1,1,10,100], 
              'gamma': [0.01,0.1,1,10],
              'kernel': ['rbf']} 
  
grid = GridSearchCV(SVC(), parameters, refit = True, verbose = 3)
  
# fitting the model for grid search
grid.fit(x_train, y_train)
predictions = grid.predict(x_test)
  
# print classification report
print(classification_report(y_test, predictions))



