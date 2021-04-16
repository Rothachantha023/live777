import os
from nltk.sentiment import SentimentIntensityAnalyzer
from approval import *
from statistics import mean
import pdb
from datetime import datetime
import csv
from textblob import TextBlob
import flair

def sentiment(path):
    sia = SentimentIntensityAnalyzer()
    flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

    ls = os.listdir(path)
    if not os.path.exists("sentiments"):
        os.makedirs("sentiments")

    sentiments = []

    with open(f'sentiments/sia.csv', 'w', newline='') as csvfile:
        fieldnames = ['date', 'pos', 'neu', 'neg']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()

        for f in ls:
            print(f)
            scores = []
            with open(f'{path}/{f}') as csvfile:
                for row in csvfile:
                    scores.append(sia.polarity_scores(row))

                    tb_sentiment = TextBlob(row).sentiment
                    
                    s = flair.data.Sentence(row)
                    flair_sentiment.predict(s)
                    flair_sentiment = s.labels[0]

                    pdb.set_trace()
                
                approval = mean(map(lambda x: x['pos'], scores))
                neutral = mean(map(lambda x: x['neu'], scores))
                disapproval = mean(map(lambda x: x['neg'], scores))
            fdate = f.split()[0].split("-")
            fdate = datetime(int(fdate[0]), int(fdate[1]), int(fdate[2]))
            sentiments.append({fdate: {'pos': approval, 'neu': neutral, 'neg': disapproval}})

            writer.writerow({'date': fdate, 'pos': approval, 'neu' : neutral, 'neg': disapproval})

    return sentiments


if __name__ == "__main__":
    ss = sentiment("nlp_tweets")
    pdb.set_trace()
    # pass