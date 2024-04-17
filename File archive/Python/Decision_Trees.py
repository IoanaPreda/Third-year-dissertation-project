
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import classification_report
from sklearn import tree

path= 'E:/Uni third/COMSOL - IP/code/20 sec/Train_data-50--2--above.csv'

##data
df = pd.read_csv(path)
# data= df.iloc[:,2:-2] 
data= df[['SKW','POW']]
task = df['Sources'] 

##splitting data for training and testing
x_train2, x_test2, y_train2, y_test2 = train_test_split(data, task, test_size = 0.2, shuffle=True)

##feature scaling
scaler = StandardScaler()
x_train2 = scaler.fit_transform(x_train2)
x_test2 = scaler.transform(x_test2)
x_train2 = pd.DataFrame(x_train2)
x_test2 = pd.DataFrame(x_test2)

##for 2 sources depth=samples_leaf-->4 for 3 sources depth=samples_leaf-->5
depth=4
samples_leaf=4
model_gini = DecisionTreeClassifier(criterion = "gini", max_depth=depth, min_samples_leaf=samples_leaf)

## fitting the classifier according to the training data
model_gini.fit(x_train2,y_train2)

## use the train data to make preditions
y_pred2=model_gini.predict(x_test2)

###Accuracy infromation
print('Accuracy: {0:0.2f}'. format(accuracy_score(y_test2, y_pred2)*100))
print('Training accuracy: {:.2f}'.format(model_gini.score(x_train2, y_train2)*100))
print(classification_report(y_test2, y_pred2))

##confusion matrix for 3 sources
# cm = confusion_matrix(y_test2, y_pred2)
# cm_matrix = pd.DataFrame(data=cm, columns=['Pred 1 source', 'Pred 2 sources','Pred 3 sources' ], 
#                                  index=['Actual 1 source', 'Actual 2 sources', 'Actual 3 sources'])
# sns.heatmap(cm_matrix, annot=True, fmt='d', cmap='YlGnBu')
# plt.tight_layout()
# plt.show()

#confusion matrix for 2 sources
cm = confusion_matrix(y_test2, y_pred2)
cm_matrix = pd.DataFrame(data=cm, columns=['Pred 1 source', 'Pred 2 sources' ], 
                                 index=['Actual 1 source', 'Actual 2 sources'])
sns.set(font_scale=1.2)
sns.heatmap(cm_matrix, annot=True, fmt='d', cmap='YlGnBu')
plt.tight_layout()
plt.show()

####################### Max Tree Depth variation plot #############################################
# ac=[]
# val=[]
# for max_d in range(1,10):
#   model =DecisionTreeClassifier(criterion = "gini",max_depth = max_d, min_samples_leaf = 5)
#   model.fit(x_train2, y_train2)
#   y_pred3=model.predict(x_test2)
#   ac.append(accuracy_score(y_test2, y_pred3)*100)
#   val.append(model.score(x_train2,y_train2)*100)
#   print('')
# plt.plot(range(1,10), ac, marker='o', label='Model Accuracy')
# plt.plot(range(1,10), val, marker='o', label= 'Training Score')
# plt.xlabel('Maximum tree depth')
# plt.ylabel('Accuracy')
# plt.legend()
# plt.grid()
# plt.show()
##################################################################################################

##10 fold validation scores and plot
kfold=KFold(n_splits=10, shuffle=True)
linear_scores = cross_val_score(model_gini, x_train2, y_train2, cv=kfold)
print('10 fold validation score:\n\n{}%'.format(linear_scores))
print('Average cross-validation score {}'.format(np.mean(linear_scores*100)))
# plt.plot(range(1,11), linear_scores)
plt.plot(range(1,11), linear_scores*100, marker='o')
plt.show()


#tree plot for 3 sources with all features
column= ['RMS', 'KURT', 'SKW', 'STD', 'POW', 'POW_Max']
target= ['1 source', '2 sources', '3 sources']
dot_data = tree.plot_tree(model_gini, feature_names=column,class_names= target, filled = True, fontsize=8)
plt.show()


