import csv
import twint
import pandas as pd
from datetime import datetime

def ngrams(input, n):
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output

dates = []
with open('realdonaldtrump.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(spamreader)
    for row in spamreader:
        date_str = row[3][:10].split("-")
        date_time = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        dates.append(date_time)
        dates = list(set(dates))

dates.sort()

dates = dates[818:]

day_ranges = ngrams(dates, 2)

c = twint.Config()
c.Search = "@realdonaldtrump"
c.Lang = "en"
c.Limit = 500
c.Popular_tweets = True

for day in day_ranges:
    c.Since = str(day[0])
    c.Until = str(day[1])
    c.Output = f"scraped_tweets/{str(day[0])}.csv"
    twint.run.Search(c)

