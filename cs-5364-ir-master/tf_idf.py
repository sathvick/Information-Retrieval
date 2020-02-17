from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_table('tweets/relevant_tweets.txt')
df.columns = ['tweet']
documents = df['tweet']

query = "love food hurricane harvey texas houston flood road drink water bottle"

tvec = TfidfVectorizer(vocabulary=query.split(' '))
tvec_tfidf = tvec.fit_transform(documents)

tvec_tfidf_as_array = np.array(tvec_tfidf.toarray())

good_documents = []
for d in tvec_tfidf_as_array:
    if sum(d) >= 0.5:
        good_documents.append(d)
## seanbon
# uniform_data = np.random.rand(10, 12)
ax = sns.heatmap(good_documents, linewidth=0)
plt.show()