from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('predicted.csv', sep="|")
text = []

doc_count = 0
music_count = 0
sport_count = 0
finance_count = 0
for index, row in df.iterrows():
    tweet_id = row['id']
    tweet = row['tweet']
    actual_label = row['class']
    predicted_label = row['predicted']

    doc_count = doc_count + 1
    if actual_label == predicted_label and actual_label == "MUSIC":
        music_count = music_count + 1
    elif actual_label != "MUSIC" and predicted_label != "MUSIC":
        music_count = music_count + 1

    if actual_label == predicted_label and actual_label == "SPORT":
        sport_count = sport_count + 1
    elif actual_label != "SPORT" and predicted_label != "SPORT":
        sport_count = sport_count + 1

    if actual_label == predicted_label and actual_label == "FINANCE":
        finance_count = finance_count + 1
    elif actual_label != "FINANCE" and predicted_label != "FINANCE":
        finance_count = finance_count + 1



# Generate a word cloud image

print("music:", (music_count / doc_count))
print("sport:", (sport_count / doc_count))
print("finance:", (finance_count / doc_count))
print("average:", ((music_count + sport_count + finance_count) / doc_count))

