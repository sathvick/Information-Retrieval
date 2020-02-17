import pandas as pd
import codecs


import csv
# with codecs.open("combined.csv","rb", "utf-8", quo) as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)

# with open('combined-text.txt', 'rb',  encoding="utf-8") as csvfile:
#     for line in csvfile:
#         print(line)
with open("combined.csv", "rb") as ins:
    with open("myconbined.csv", "w") as writer:
        header = True
        end_line = False
        complete_line = ''
        counter = 0
        start_line = ''
        for line in ins:
            if header == True:
                header = False
                continue
            my_string = line.decode("utf-8", "ignore")
            my_string = my_string.strip()
            if my_string.startWith("Finance") or my_string.startWith("Sport") or my_string.startWith("Music"):
                print("test")
                if len(start_line) > 0:
                    complete_line = start_line
                start_line = my_string
            else:
                complete_line = start_line + line
            if len(complete_line) > 0:
                print("line:", complete_line)
                complete_line = ''
                start_line = ''
                counter = counter + 1
                writer.write(complete_line + "\n")

            if counter > 20:
                break
# print(row)
# df = pd.read_csv("combined.csv", sep=",", encoding ='utf8',quotechar='"' )
# for _, row in df.iterrows():
#     print("test")