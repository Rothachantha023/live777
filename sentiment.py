import os
from nltk.sentiment import SentimentIntensityAnalyzer
from approval import *
from statistics import mean
import pdb
from datetime import datetime

def sentiment(path):
    sia = SentimentIntensityAnalyzer()

    ls = os.listdir(path)

    sentiments = []

    for f in ls:
        print(f)
        scores = []
        with open(f'{path}/{f}') as csvfile:
            for row in csvfile:
                scores.append(sia.polarity_scores(row))
            
            approval = mean(map(lambda x: x['pos'], scores))
            neutral = mean(map(lambda x: x['neu'], scores))
            disapproval = mean(map(lambda x: x['neg'], scores))
        fdate = f.split()[0].split("-")
        fdate = datetime(int(fdate[0]), int(fdate[1]), int(fdate[2]))
        sentiments.append({fdate: {'pos': approval, 'neu': neutral, 'neg': disapproval}})
    return sentiments


if __name__ == "__main__":
    ss = sentiment("nlp_tweets")
    pdb.set_trace()
    # pass