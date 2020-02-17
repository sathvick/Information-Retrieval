import csv
from datetime import datetime

filepath = '/home/long/DDL/project-data/Houseton-Harvey/Houston-Harvey'

input_files = [
    # 'sample.txt'
    '2017_08_26_stream.txt',
    '2017_08_27_stream.txt',
    '2017_08_28_stream.txt',
    '2017_08_29_stream.txt',
    '2017_08_30_stream.txt',
]

def remove_newline(dataArr):
    result = []
    for d in dataArr:
        d = d.replace("\n", '', 10)
        d = d.replace("\r", '', 10)

        result.append(d)

    return result

for input_f in input_files:

    with open(filepath + '/' + input_f) as f:

        with open(input_f + '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["tweet_id", "datetime", "city", "state", "country", "gps", "polygon", "tweet"])

            for line in f:
                parts = line.split('\x01')

                if len(parts) < 24:
                    print("bad tweet:", line)
                    continue

                id = parts[0]
                tweet = parts[1]

                tweet = tweet.lower()
                if 'harvey' not in tweet and 'hurricane' not in tweet:
                    continue


                gps = parts[2]
                city = parts[14]
                country = parts[16]

                polygon = parts[19]
                date =parts[6]

                datetime_object = datetime.strptime(date, "%a %b %d %H:%M:%S %Z %Y")
                datetime_string = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
                state = parts[23]

                d = remove_newline([id, datetime_string, city, state, country, gps, polygon, tweet])
                writer.writerow(d)
