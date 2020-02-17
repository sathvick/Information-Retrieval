from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import codecs

query = "love food hurricane harvey texas houston flood road drink water bottle"

stemmer = SnowballStemmer("english")
stop_words = stopwords.words('english')
extra_stopwords = ['@', '-', '_', '','i',"i'm", '&',"it","la","the","de","en","que","this","el","floyd"]

my_stopwords = stop_words + extra_stopwords

## tokenization and remove stopwords
query_terms = query.split(" ")
my_query = []
for t in query_terms:
    if t not in my_stopwords:
        stemmer.stem(t)
        my_query.append(t)

## stem words
print(' '.join(my_query))

## remove tweets not containing any term in the queries


df = pd.read_csv('tweets/clean_tweets.csv', sep=',')
df = df.dropna()

tweets = df['tweet']
relevant_tweets = []
for tweet in tweets:
    # check if any term of query in tweet
    contain_q = False
    for q in my_query:
        if q in tweet:
            contain_q = True
            print("found tweet", tweet)
            break
    # drop the tweet if it does not contain any term in the query
    if contain_q == True:
        relevant_tweets.append(tweet)

print("relevant tweets count:", len(relevant_tweets))
with codecs.open('tweets/relevant_tweets.txt', 'w', "utf-8") as f:
    for t in relevant_tweets:
        f.write(t + '\r\n')



