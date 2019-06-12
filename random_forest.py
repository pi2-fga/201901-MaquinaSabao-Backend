import numpy as np
from sklearn import svm, preprocessing, neighbors
from numpy import genfromtxt
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from invoice2data import extract_data
from tabula import read_pdf
from sklearn.ensemble import AdaBoostClassifier
import math
from sklearn.model_selection import RandomizedSearchCV

train = genfromtxt('ml-prove/train.csv', delimiter=',')
test = genfromtxt('ml-prove/test.csv', delimiter=',')
validation = genfromtxt('ml-prove/validation.csv', delimiter=',')

# Separando targets e features:

validation_X = validation[:,0:-6]
validation_y = validation[:,-6:]

X_train = train[:,0:-6]
y_train_1 = train[:,-6:-5]
y_train_2 = train[:,-5:-4]
y_train_3 = train[:,-4:-3]
y_train_4 = train[:,-3:-2]
y_train_5 = train[:,-2:-1]
y_train_6 = train[:,-1:]

X_test = test[:,0:-6]
y_test_1 = test[:,-6:-5]
y_test_2 = test[:,-5:-4]
y_test_3 = test[:,-4:-3]
y_test_4 = test[:,-3:-2]
y_test_5 = test[:,-2:-1]
y_test_6 = test[:,-1:]


#-----------------RandomForestClassifier-----------------#

# quantidade de combinações de hyperparametros = 4320 * 6

params = {
    'bootstrap': [True, False],
    'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
    'max_features': ['auto', 'sqrt'],
    'min_samples_leaf': [1, 2, 4],
    'min_samples_split': [2, 5, 10],
    'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
}

clf = RandomForestClassifier()

rfc = RandomizedSearchCV(
    estimator = clf, 
    param_distributions = params, 
    n_iter = 100,
    cv = 3,
    verbose=2,
    random_state=42,
    n_jobs = -1
)

dict_params = []
accuracy_list = []
time = []


#--------------H1------------------#

rfc.fit(X_train, y_train_1.ravel())

dict_params.append(rfc.best_params_)

score = rfc.score(X_test, y_test_1)

accuracy = score
accuracy_list.append(score)
time.append(rfc.refit_time_)

#--------------H2-----------------#

rfc.fit(X_train, y_train_2.ravel())

dict_params.append(rfc.best_params_)

score = rfc.score(X_test, y_test_2)

accuracy += score
accuracy_list.append(score)
time.append(rfc.refit_time_)

#--------------H3-----------------#

rfc.fit(X_train, y_train_3.ravel())

dict_params.append(rfc.best_params_)

score = rfc.score(X_test, y_test_3)

accuracy += score
accuracy_list.append(score)
time.append(rfc.refit_time_)

#--------------H4-----------------#

rfc.fit(X_train, y_train_4.ravel())

dict_params.append(rfc.best_params_)

score = rfc.score(X_test, y_test_4)

accuracy += score
accuracy_list.append(score)
time.append(rfc.refit_time_)

#--------------H5-----------------#

rfc.fit(X_train, y_train_5.ravel())

dict_params.append(rfc.best_params_)

score = rfc.score(X_test, y_test_5)

accuracy += score
accuracy_list.append(score)
time.append(rfc.refit_time_)

#-----------------H0-----------------#

rfc.fit(X_train, y_train_6.ravel())

dict_params.append(rfc.best_params_)

score = rfc.score(X_test, y_test_6)

accuracy += score
accuracy_list.append(score)
time.append(rfc.refit_time_)

print("--------")
print(accuracy/6.0)
print("--------")
print(dict_params)
print("--------")
print(accuracy_list)
print("--------")
print(time)
print("--------")
