from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns



df = pd.read_table('tweets/relevant_tweets.txt')
df.columns = ['tweet']
documents = df['tweet']

query = "love food hurricane harvey texas houston flood road drink water bottle"

cvec = CountVectorizer(vocabulary=query.split(' '))

document_term_matrix = cvec.fit_transform(documents)
# document_term_matrix = cvec.fit_transform(['love food is so good', 'hurricane is happing in texas'])
document_term_matrix_as_array = np.array(document_term_matrix.toarray())
print(document_term_matrix_as_array)


good_documents = []
for d in document_term_matrix_as_array:
    if sum(d) >= 4:
        good_documents.append(d)
## seanbon
# uniform_data = np.random.rand(10, 12)
ax = sns.heatmap(good_documents, linewidth=0)
plt.show()