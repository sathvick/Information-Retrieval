from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('predicted.csv', sep="|")
text = []
for index, row in df.iterrows():
    tweet_id = row['id']
    tweet = row['tweet']
    actual_label = row['class']
    predicted_label = row['predicted']

    if predicted_label == "FINANCE":
        text.append(tweet)


# Generate a word cloud image
wordcloud = WordCloud(background_color="black", collocations=False).generate(' '.join(text))
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

