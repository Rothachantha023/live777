import os
import csv
import twint
import pandas as pd
from datetime import datetime

def ngrams(input, n):
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output

def get_matching_tweets_by_date():
    dates = []
    with open('realdonaldtrump.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:
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

def clean_csvs(path):
    if not os.path.exists("cleaned_tweets"):
        os.makedirs("cleaned_tweets")

    ls = os.listdir(path)
    for f in ls:
        with open(f'{path}/{f}') as csvfile:

            writefile = open(f"cleaned_tweets/{f}_cleaned.txt", "w")

            for row in csvfile:
                split = row.split()
                tweet = " ".join(split[5:])
                tidy_tweet = tweet.strip().encode('ascii', 'ignore')
                writefile.write(str(tidy_tweet) + "\n")
        writefile.close()

if __name__ == "__main__":
    clean_csvs("scraped_tweets")
    
