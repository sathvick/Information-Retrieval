#!/usr/bin/env python
import os

from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('tweets/filtered_data.txt', sep='\000')
df.columns =['id','tweet']

text = []
for tweet in df['tweet']:
    tweet = bytes(tweet, 'utf-8').decode()
    text.append(tweet)


# Generate a word cloud image
wordcloud = WordCloud(background_color="white", collocations=False).generate(' '.join(text))
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

