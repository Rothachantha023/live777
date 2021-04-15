import os
import csv
import twint
import pandas as pd
from datetime import datetime
import re
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize
import inflect

def ngrams(input, n):
    """
    Generate n-grams of size n from a list of input
    """
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output

def get_matching_tweets_by_date():
    """
    Find tweets mentioning c.Search within date ranges mentioned in realdonaldtrump.csv
    """
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
    """
    Clean ASCII emoji stuff, save to cleaned_tweets/.
    """
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

def nlp_clean():
    """
    Perform NLP text normalization
    """
    if not os.path.exists("nlp_tweets"):
        os.makedirs("nlp_tweets")

    ls = os.listdir(f'cleaned_tweets')
    for f in ls:
        with open(f'cleaned_tweets/{f}') as csvfile:
            writefile = open(f"nlp_tweets/{f}_ready.txt", "w")
            print("Processing " + f)

            for row in csvfile:
                output = ""

                # Filter out b' binary
                text = re.sub(r'b\'', '', row)
                text = re.sub(r'b\"', '', text)

                # Filter out URLs
                text = re.sub(r"http\S+", '', text)

                # Filter out @
                text = re.sub(r'@\S+', '', text)

                # Filter out punctuation
                text = re.sub(r'[^\w\s]', '', text)

                # Replace numbers with text
                p = inflect.engine()
                words = word_tokenize(text)
                new_words = []
                for word in words:
                    try:
                        if word.isdigit():
                            new_word = p.number_to_words(word)
                            new_words.append(new_word)
                        else:
                            new_words.append(word)
                    except:
                        print("It's too big! :o")

                text = new_words

                # Lowercase
                new_words = []
                for word in text:
                    new_word = word.lower()
                    new_words.append(new_word)
                
                text = new_words

                # Filter out stopwords
                new_words = []
                for word in text:
                    if word not in stopwords.words('english'):
                        new_words.append(word)

                text = new_words

                writefile.write(" ".join(text) + "\n")
        writefile.close()
    


if __name__ == "__main__":
    # clean_csvs("scraped_tweets")
    nlp_clean()
    
