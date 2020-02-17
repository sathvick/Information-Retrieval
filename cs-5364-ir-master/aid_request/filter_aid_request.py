import csv
from datetime import datetime

input_files = [
    # 'sample.txt'
    'aid_2017_08_26_stream.txt.csv',
    'aid_2017_08_27_stream.txt.csv',
    'aid_2017_08_28_stream.txt.csv',
    'aid_2017_08_29_stream.txt.csv',
    'aid_2017_08_30_stream.txt.csv',
]

def contain_offering_help_terms(tweet):
    terms = [
        "if", "affect", "donate",  "pray", "volunteer"
        "relief", "recovery","to help", "giv", "victim",
        "need to"
    ]

    for t in terms:

        if t in tweet:
            return True

    return False


def is_aid_request(tweet):
    if contain_offering_help_terms(tweet=tweet):
        return False

    if "please" in tweet:
        return True

    # offering aid
    if "donate" in tweet or "donation" in tweet or "can help" in tweet or "had aid" in tweet \
            or "support" in tweet:
        return False

    if "help" in tweet or "need" in tweet or "demand" in tweet or " aid" in tweet or "urg" in tweet:
        return True

    return False

for input_f in input_files:

    with open(input_f, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter='|', quotechar='"')
        next(reader)
        with open("aid_request_" + input_f, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["tweet"])

            for row in reader:

                tweet = row[7]
                if is_aid_request(tweet=tweet):
                    writer.writerow([tweet])
