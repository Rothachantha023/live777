import os
from nltk.sentiment import SentimentIntensityAnalyzer
from approval import *

def sentiment(path):
    sia = SentimentIntensityAnalyzer()

    ls = os.listdir(path)
    for f in ls:
        with open(f'{path}/{f}') as csvfile:
            for row in csvfile:
                print(sia.polarity_scores(row))
        break


if __name__ == "__main__":
    sentiment("cleaned_tweets")