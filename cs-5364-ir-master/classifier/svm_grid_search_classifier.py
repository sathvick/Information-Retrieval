from pandas.core.series import Series
from sklearn.pipeline import Pipeline #pipeline to implement steps in series
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer #convert text comment into a numeric vector
from sklearn.feature_extraction.text import TfidfTransformer #use TF IDF transformer to change text vector created by count vectorizer
from sklearn.svm import SVC# Support Vector Machine
from sklearn.datasets import fetch_20newsgroups
from sklearn import metrics
from sklearn.pipeline import Pipeline

from sklearn.model_selection import GridSearchCV

# df_train = pd.read_csv("hw_train_2_classes.csv", sep="|")
# df_test = pd.read_csv("hw_test_2_classes.csv", sep="|")

df_train = pd.read_csv("../aid_request/train_hw4.csv", sep="|")

df_test = pd.read_csv("../aid_request/test_hw4.csv", sep="|")


#Seperate data into feature and results
X_train, y_train = df_train['tweet'].tolist(), df_train['label'].tolist()
X_test, y_test = df_test['tweet'].tolist(), df_test['label'].tolist()

voc = []
for t in (X_train + X_test):
    terms = t.split()
    voc.extend(terms)
cvec = CountVectorizer(vocabulary=set(voc))
#
X_train_counts = cvec.fit_transform(X_train)
X_test_counts = cvec.fit_transform(X_test)

text_clf = SVC(kernel='linear')

X_train = X_train_counts
X_test = X_test_counts

parameters = {'C': [1, 10, 100, 1000], 'gamma': ["auto", 1, 0.1, 0.001, 0.0001], 'kernel': ['linear', 'rbf']}


gs_clf = GridSearchCV(text_clf, parameters, refit=True, n_jobs=-1, verbose=2)
gs_clf = gs_clf.fit(X_train, y_train)

print("best score: ", gs_clf.best_score_)
print("best params: ", gs_clf.best_params_)

#predict class form test data
predicted = gs_clf.predict(X_test)

print(predicted)
print("Accuracy: {}%".format(gs_clf.score(X_test, y_test) * 100 ))

print(metrics.classification_report(y_test, predicted))

print(y_test)

print(metrics.confusion_matrix(y_test, predicted))

df_test["predicted_class"] = Series(predicted, index=df_test.index)

df_test.to_csv("../aid_request/grid_search_predicted.csv", sep="|", quotechar='"', index=False)

print(gs_clf.cv_results_)
