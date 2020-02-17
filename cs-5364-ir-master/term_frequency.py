from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import operator

df = pd.read_table('tweets/relevant_tweets.txt')
df.columns = ['tweet']
extra_stopwords = ['@', '-', '_','—', '','i',"i'm", '&',"it","la","the","de","en","que","this","el","floyd"]

tweets = df['tweet']

terms = dict()
for tweet in tweets:
    tweet = bytes(tweet, 'utf-8').decode()
    tweet_terms = tweet.split(" ")
    for term in tweet_terms:
        if term in extra_stopwords:
            continue
        if term in terms:
            terms[term] += 1
        else:
            terms[term] = 1

# extract high frequency terms
min_threshold=1000
frequency_list = terms.keys()
results = []
for word in frequency_list:
    if min_threshold is not None:
        if terms[word] < min_threshold:
            continue
    tuple = (word, terms[word])
    results.append(tuple)

byFreq = sorted(results, key=lambda word: word[1], reverse=True)
print("terms:", len(byFreq))

## plot frequent terms using 10 top words
sorted_wfreq = byFreq[0:20]
final_wfreq = dict()
for word, freq in sorted_wfreq:
    final_wfreq[word] = freq

sorted_wfreq = sorted(final_wfreq.items(), key=operator.itemgetter(1))
words_names = []
words_count = []

for word, freq in sorted_wfreq:
    words_names.append(word)
    words_count.append(freq)

show_plot = True
if show_plot == True:
    #
    fig, ax = plt.subplots()
    width = 0.56 # the width of the bars
    ind = np.arange(len(words_count))  # the x locations for the groups
    ax.barh(ind, words_count, width, color="#3366cc")
    ax.set_yticks(ind+width/2)
    ax.set_yticklabels(words_names, minor=False)
    plt.title('Word Frequency')
    plt.xlabel('Frequencies')
    plt.ylabel('Words')
    for i, v in enumerate(words_count):
        ax.text(v + 0.2, i - .15, str(v), color='black', fontweight='bold')
    plt.show()
