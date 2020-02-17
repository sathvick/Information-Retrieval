import codecs
import pandas as pd
import csv






import codecs

## Stepp 1. Read line by line
tweet_count = 0
with codecs.open("hurricane/09_15_filtered.csv", "w") as f:
    with open("hurricane/09-15-18_0.csv") as ins:
        counter = 0
        for line in ins:
            ## Step 2. Extract important content per line
            parts = line.split("|")
            if len(parts) < 2:
                continue
            tweet_id = parts[0]
            tweet_text = parts[1]
            if len(tweet_text) < 10:
                continue
            tweet_class = parts[2]
            # if len(parts)>= 3:
            #     tweet_geo = parts[2]
            # else:
            #     tweet_geo = ''
            #
            # if len(parts)>= 6:
            #     tweet_date = parts[6]
            # else:
            #     tweet_date = ''

            lower_case_tweet = tweet_text.lower()
            print('id：', tweet_id, "text:", lower_case_tweet, tweet_class)

            ##Step 3. Write important content to other file.
            # f.write(tweet_id + '\000' + tweet_date + '\000' + tweet_text + '\r\n')
            f.write(tweet_id + '\000' + lower_case_tweet +'\000' + tweet_class+'\r')
            tweet_count+= 1

print("Total tweet count", tweet_count)
