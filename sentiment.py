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
    flair_model = flair.models.TextClassifier.load('en-sentiment')

    ls = os.listdir(path)
    if not os.path.exists("sentiments"):
        os.makedirs("sentiments")

    sia_normalized = []
    tb_normalized = []
    fl_normalized = []

    for f in ls:
        print(f)
        sia_scores = []
        tb_scores = []
        fl_scores = []

        with open(f'{path}/{f}') as csvfile:
            for row in csvfile:
                if row != "\n":
                    # NLTK
                    nltk_sentiment = sia.polarity_scores(row)
                    sia_scores.append(nltk_sentiment)

                    #TEXTBLOB
                    textblob_sentiment = TextBlob(row).sentiment
                    tb_scores.append(textblob_sentiment)

                    #FLAIR
                    flair_sentence = flair.data.Sentence(row)
                    flair_model.predict(flair_sentence)
                    flair_sentiment = flair_sentence.labels[0]
                    fl_scores.append(flair_sentiment)

        fdate = f.split()[0].split("-")
        fdate = datetime(int(fdate[0]), int(fdate[1]), int(fdate[2]))

        #NLTK
        sia_pos = len(list(filter(lambda x: x['pos'] > x['neu'], sia_scores))) / len(sia_scores)
        sia_neu = len(list(filter(lambda x: x['neu'] > x['neg'] and x['neu'] > x['pos'], sia_scores))) / len(sia_scores)
        sia_neg = len(list(filter(lambda x: x['neg'] > x['neu'], sia_scores))) / len(sia_scores)
        sia_normalized.append({'date': fdate, 'pos': sia_pos, 'neu' : sia_neu, 'neg': sia_neg})

        #TEXTBLOB
        tb_pos = []
        tb_neu = []
        tb_neg = []
        for tb in tb_scores:
            if tb.polarity < -0.5:
                tb_neg.append(tb)
            elif tb.polarity < 0.5:
                tb_neu.append(tb)
            else:
                tb_pos.append(tb)
        
        tb_pos = len(tb_pos) / len(tb_scores)
        tb_neu = len(tb_neu) / len(tb_scores)
        tb_neg = len(tb_neg) / len(tb_scores)
        tb_normalized.append({'date': fdate, 'pos': tb_pos, 'neu' : tb_neu, 'neg': tb_neg})

        #FLAIR
        fl_pos = []
        fl_neu = []
        fl_neg = []
        for fl in fl_scores:
            if fl.score > 0.5 and fl.value == 'NEGATIVE':
                fl_neg.append(fl)
            elif fl.score > 0.5 and fl.value == 'POSITIVE':
                fl_pos.append(fl)
            else:
                fl_neu.append(fl)

        fl_pos = len(fl_pos) / len(fl_scores)
        fl_neu = len(fl_neu) / len(fl_scores)
        fl_neg = len(fl_neg) / len(fl_scores)
        fl_normalized.append({'date': fdate, 'pos': fl_pos, 'neu' : fl_neu, 'neg': fl_neg})

        # pdb.set_trace()


    with open(f'sentiments/sia.csv', 'w', newline='') as csvfile:
        fieldnames = ['date', 'pos', 'neu', 'neg']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(sia_normalized)
    with open(f'sentiments/tb.csv', 'w', newline='') as csvfile:
        fieldnames = ['date', 'pos', 'neu', 'neg']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(tb_normalized)
    with open(f'sentiments/fl.csv', 'w', newline='') as csvfile:
        fieldnames = ['date', 'pos', 'neu', 'neg']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(fl_normalized)


if __name__ == "__main__":
    sentiment("nlp_tweets")