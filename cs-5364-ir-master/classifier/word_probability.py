import pandas as pd
import numpy as np
from pandas.core.series import Series

from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score

df = pd.read_csv("hw_train.csv", sep="|", header=0)

word_frequency = dict()
class_frequency = dict()
query_x = None
doc_count = 0
doc_class_frequency = dict()
for index, row in df.iterrows():
    tweet = row.iloc[1]
    label = row.iloc[2]
    # counting documents and documents per class for class probability
    doc_count = doc_count + 1
    if label not in doc_class_frequency:
        doc_class_frequency[label] = 0
    doc_class_frequency[label] = doc_class_frequency[label] + 1

    if label not in class_frequency:
        class_frequency[label] = dict()
        class_frequency[label + "-count"] = 0
    # counting words per class for word probabilities
    current_class = class_frequency[label]
    if type(tweet) is float:
        print("test")
    words = tweet.split()
    for w in words:

        class_frequency[label + "-count"] = class_frequency[label + "-count"] + 1
        if w not in current_class:
            current_class[w] = 0
        current_class[w] = current_class[w] + 1

        if w not in word_frequency:
            word_frequency[w] = 0

        word_frequency[w] = word_frequency[w] + 1

voc_size = len(word_frequency)
# print(voc_size)
## compute word probability ###
# for label, word_class_frequency in class_frequency.items():
#     if "count" in label:
#         continue
#     word_count = class_frequency[label + "-count"]
#     print("class:", label, "; word count:", word_count)
#
#     x_words = list(set(query_x.split()))
#     for w, freq in word_class_frequency.items():
#         word_prob = (freq + 1) / (word_count + voc_size)
#         print("p(", w, "/", label, ")=", word_prob)
#
#         if w in x_words:
#             x_words.remove(w)
#     for w in x_words:
#         word_prob = (0 + 1) / (word_count + voc_size)
#         print("p(", w, "/", label, ")=", word_prob)

## compute the query class ###

# sorted_by_value = sorted(class_frequency["MUSIC"].items(), key=lambda kv: kv[1])
# count = 0
# s = [(k, class_frequency["FINANCE"][k]) for k in sorted(class_frequency["FINANCE"], key=class_frequency["FINANCE"].get, reverse=True)]
# for k, v in s:
#    print("key:", k, "; val:", v)
#    count = count + 1
#    if count > 9:
#        break


df = pd.read_csv("hw_test.csv", sep="|", header=0)
y_true = []
y_pred = []
for _, row in df.iterrows():
    query_x = row.iloc[1]
    query_label = row.iloc[2]
    y_true.append(query_label)
    x_words = list(set(query_x.split()))
    max_prob = 0
    max_class = None
    for label, word_class_frequency in class_frequency.items():
        if "count" in label:
            continue
        word_count = class_frequency[label + "-count"]
        print("class:", label, "; word count:", word_count)

        word_probs = dict()
        for w in x_words:
            word_fre = 0
            if w in word_class_frequency:
                word_fre = word_class_frequency[w]
            word_prob = (word_fre + 1) / (word_count + voc_size)
            print("p(", w, "/", label, ")=", word_prob)
            if w not in word_probs:
                word_probs[w] = word_prob

        my_prob = doc_class_frequency[label] / doc_count
        for w in query_x.split():
            my_prob = my_prob*word_probs[w]

        print("label:", label, "; prob:", my_prob)
        if max_prob < my_prob:
            max_prob = my_prob
            max_class = label

    print()
    print("Query:", query_x)
    print("predicted class:", max_class, "; prob:", max_prob, "; actual:", query_label)
    y_pred.append(max_class)

df['predicted'] = Series(np.array(y_pred), index=df.index)

df.to_csv("predicted.csv", sep="|", index=False)

precision, recall, f_score, _ = precision_recall_fscore_support(y_true=y_true, y_pred=y_pred,
                                                                labels=['MUSIC', 'SPORT', 'FINANCE'], average="weighted")
accuracy = accuracy_score(y_true=y_true, y_pred=y_pred)
print("accuracy:", accuracy, "precision:", precision, "; recall:", recall, "; f-score:", f_score)

