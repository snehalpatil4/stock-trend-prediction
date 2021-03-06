# -*- coding: utf-8 -*-
"""LP-1_DMW_project_code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R5Ax2dSKVhUaAOR2vl9qpztHSbvi8ivG
"""

!wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
 !ls
 !tar xvzf ta-lib-0.4.0-src.tar.gz
 import os
 os.chdir('ta-lib')
 !./configure --prefix=/usr
 !make
 !make install
 os.chdir('../')
 !pip install TA-Lib

"""**STOCK  TREND PREDICTION** 
DMW Mini Project-LP-1
* NAME-Harsh Munot(BECOB212)
* NAME-Payal Narkhede(BECOB214)
* NAME-Snehal Patil(BECOB226)
```
DATASET DETAILS
```
Dataset- KOTAKBANK.csv from NIFTY-50 dataset on Kaggle 
There are 4863 entries from 2000 to 2020
There are total 14 cloumns
We have tried to build a model which can predict the uptrend i.e. 1 or downTrend i.e. 0.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df=pd.read_csv("/content/KOTAKBANK.csv",index_col=[0])
df.index=pd.to_datetime(df.index)
df.head()

df=df.drop(['Symbol','Series','Prev Close','VWAP','Turnover','Trades','Deliverable Volume','%Deliverble'],axis=1)
df.head()

df.info()

df.Close.plot(figsize=(15,7))
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title('KOTAKBANK')
plt.grid()
plt.show()

df=df['2004-01-01':'2020-10-30']

df.Close.plot(figsize=(15,7))
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title('KOTAKBANK')
plt.grid()
plt.show()

import talib as ta
df['RSI']=ta.RSI(df['Close'].values,timeperiod=14)
df['DIFF1']=df['Close'].diff().values
df['DIFF2']=df['Close'].diff(2).values
df['DIFF3']=df['Close'].diff(3).values
df['DIFF4']=df['Close'].diff(4).values
print(df.head())
df.tail()

df['Trends']=np.where(df.Close.shift(-1)>df.Close,1,0)
print(df.head(15))
df.tail(15)

print(df['Trends'].count())
print(df['Trends'].sum())

df.dropna(inplace=True)
predictor_list=['RSI','DIFF1','DIFF2','DIFF3','DIFF4']
X=df[predictor_list]
y=df['Trends']
y.tail()

print(df['Trends'].count())
df['Trends'].sum()

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)
print(X_train.shape,X_test.shape)
print(y_train.shape,y_test.shape)

print(X_train,X_test)
print(y_train,y_test)

from sklearn.tree import DecisionTreeClassifier
clf=DecisionTreeClassifier(criterion='gini',max_depth=3,random_state=20,min_samples_leaf=5)
model=clf.fit(X_train,y_train)

print(accuracy_score(y_test,model.predict(X_test),normalize=True)*100)

from sklearn.model_selection import KFold
kf=KFold(n_splits=5,shuffle=False)
kf.split(X)

from sklearn.metrics import accuracy_score
accuracy_model=[]
for train_index,test_index in kf.split(X):
  X_train,X_test=X.iloc[train_index],X.iloc[test_index]
  y_train,y_test=y[train_index],y[test_index]
  model=clf.fit(X_train,y_train)
  accuracy_model.append(accuracy_score(y_test,model.predict(X_test),normalize=True)*100)
print(accuracy_model)

scores = pd.DataFrame(accuracy_model,columns=['Scores'])
sns.set(style="white", rc={"lines.linewidth": 3})
sns.displot(scores)
plt.show()
sns.set()

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
cm = confusion_matrix(y_test, y_pred)
print("CONFUSION MATRIX \n",cm)

from sklearn.metrics import classification_report
y_pred=model.predict(X_test)
report=classification_report(y_test,y_pred)
print(report)

from scipy.stats import sem
from numpy import mean
from numpy import std
from sklearn.datasets import make_classification
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from matplotlib import pyplot
model_NB = GaussianNB()
model_NB.fit(X_train, y_train)

# evaluate a model with a given number of repeats
def evaluate_model(X, y, repeats):
	cv = RepeatedKFold(n_splits=10, n_repeats=repeats, random_state=1)
	scores_NB = cross_val_score(model_NB, X, y, scoring='accuracy', cv=cv, n_jobs=-1)
	return scores_NB

# create dataset

repeats = range(1,16)
results = list()
for r in repeats:
	scores_NB = evaluate_model(X, y, r)
	results.append(scores_NB)
sns.displot(scores_NB)

y_pred_NB = model_NB.predict(X_test)
cm = confusion_matrix(y_test, y_pred_NB)
print(cm)
report=classification_report(y_test,y_pred_NB)
print(report)

# Commented out IPython magic to ensure Python compatibility.
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt 
# %matplotlib inline
k_range = range(1, 31)
k_scores = []
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X, y, cv=10, scoring='accuracy')
    k_scores.append(scores.mean())
sns.distplot(k_scores)

y_pred_knn= classifier_knearest.predict(X_test)
cm = confusion_matrix(y_test, y_pred_knn)
print(cm)
report=classification_report(y_test,y_pred_knn)
print(report)