import pandas as pd
from pandas.core.series import Series
from sklearn.model_selection import train_test_split
import numpy as np
import csv
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


df_aid = pd.read_csv("aid_2017_08_28_stream.txt.csv", sep="|", quotechar='"', header=0)
df_aid.drop(columns=["datetime", "city", "state", "country", "gps", "polygon"], inplace=True)
df_aid['label'] = Series([1]*len(df_aid), index=df_aid.index)

train_aid, test_aid = train_test_split(df_aid, test_size=0.2)

df_non_aid = pd.read_csv("non_aid_2017_08_28_stream.txt.csv", sep="|", quotechar='"', header=0)
df_non_aid.drop(columns=["datetime", "city", "state", "country", "gps", "polygon"], inplace=True)
df_non_aid['label'] = Series([0]*len(df_non_aid), index=df_non_aid.index)
train_non_aid, test_non_aid = train_test_split(df_non_aid, test_size=0.2)


train = pd.concat([train_aid, train_non_aid], ignore_index=True, axis=0)
test = pd.concat([test_aid, test_non_aid], ignore_index=True, axis=0)

stop_words = stopwords.words('english')
extra_stopwords = ['@', '-', '_', '','i',"i'm", '&',"it","la","the","de","en","que","this","el","floyd"]
my_stopwords = stop_words + extra_stopwords
stemmer = SnowballStemmer("english")

start_with_stopwords = ["@", '#', 'http']


def is_stop_word(word):
    # if word in my_stopwords:
    #     return True

    # startswith test
    for st in start_with_stopwords:
        if word.startswith(st):
            return True

    return False


def pre_process_text(tweet):
    # words = [stemmer.stem(word.lower()) for word in tweet.split() if not is_stop_word(word.lower())]
    words = [word.lower() for word in tweet.split() if not is_stop_word(word.lower())]

    return ' '.join(words)


def clean_text_and_write_to_file(filename, df):

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["tweet_id", "tweet", "label"])

        for idx, row in df.iterrows():

            if idx % 50 == 0:
                print(filename, ", done processing 50 tweets: ", idx)

            tweet_id = row["tweet_id"]
            tweet = row["tweet"]

            try:
                label = int(row["label"])
            except:
                print(filename, ", bad tweet ", id, "; tweet:", tweet)
                continue

            tweet = pre_process_text(tweet=tweet)
            if tweet.strip() == '':
                continue

            writer.writerow([tweet_id, tweet, label])


clean_text_and_write_to_file('no_train_hw4.csv', train)
clean_text_and_write_to_file('no_test_hw4.csv', test)
