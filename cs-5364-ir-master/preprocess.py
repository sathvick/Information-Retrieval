from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


df = pd.read_csv('tweets/filtered_data.txt', sep='\000')
df.columns =['id','tweet']

stemmer = SnowballStemmer("english")
stop_words = stopwords.words('english')
extra_stopwords = ['@', '-', '_', '','i',"i'm", '&',"it","la","the","de","en","que","this","el","floyd"]

my_stopwords = stop_words + extra_stopwords

## tokenization and remove stopwords
df['tweet'] = df['tweet'].apply(lambda x: ' '.join([word for word in x.split(' ') if word not in my_stopwords]))
## stem words
df['tweet'] = df['tweet'].apply(lambda x: ' '.join([stemmer.stem(y) for y in x.split(' ')]))
df['tweet'].head()

df.to_csv("tweets/clean_tweets.csv", mode = 'w', index=False)