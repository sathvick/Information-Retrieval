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

# voc = []
# for t in (X_train + X_test):
#     terms = t.split()
#     voc.extend(terms)
#
# cvec = CountVectorizer(vocabulary=set(voc))
# #
# X_train_counts = cvec.fit_transform(X_train)
# X_test_counts = cvec.fit_transform(X_test)

#Use pipeline to carry out steps in sequence with a single object
#SVM's rbf kernel gives highest accuracy in this classification problem.
# text_clf = SVC(kernel='rbf')
# text_clf = SVC(kernel='poly')
# text_clf = SVC(kernel='linear')

#train model

text_clf = Pipeline([
     ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SVC(kernel='rbf', C=100, gamma='auto')),
])



# X_train = X_train_counts
# X_test = X_test_counts

text_clf.fit(X_train, y_train)

#predict class form test data
predicted = text_clf.predict(X_test)

print(predicted)
print("Accuracy: {}%".format(text_clf.score(X_test, y_test) * 100 ))

print(metrics.classification_report(y_test, predicted))

print(y_test)

print(metrics.confusion_matrix(y_test, predicted))

df_test["predicted_class"] = Series(predicted, index=df_test.index)

df_test.to_csv("../aid_request/rbf_predicted.csv", sep="|", quotechar='"', index=False)

