from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('../aid_request/processed_count_vector_predicted.csv', sep="|", quotechar='"', header=0)
word_counts = {}
for index, row in df.iterrows():
    tweet_id = row['tweet_id']
    tweet = row['tweet']
    actual_label = row['label']
    predicted_label = row['predicted_class']

    if actual_label == 1:
        words = tweet.split()
        for w in words:
            w = w.strip(',')
            w = w.strip('!')
            if w not in word_counts:
                word_counts[w] = 0
            word_counts[w] = word_counts[w] + 1


# x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
x = word_counts
sorted_by_value = sorted(x.items(), key=lambda kv: kv[1], reverse=True)

count = 0
new_dict = dict()
for k, v in sorted_by_value:
    if count > 15:
        break
    new_dict[k] = v
    count = count + 1

print(new_dict)
sorted_by_value = sorted(new_dict.items(), key=lambda kv: kv[1], reverse=False)

print(sorted_by_value)
my_x = []
my_count = []
for k, v in sorted_by_value:
    my_x.append(k)
    my_count.append(v)

print("my_x", my_x)
print("my_count", my_count)

x_pos = [i for i, _ in enumerate(my_x)]


plt.barh(x_pos, my_count, color='green')
plt.ylabel("Frequency")
plt.xlabel("Term")
plt.title("Term frequency")

plt.yticks(x_pos, my_x)

plt.show()
