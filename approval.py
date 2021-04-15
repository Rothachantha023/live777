import csv
import os
from datetime import datetime
import pdb
from statistics import mean

def approval():
    ls = os.listdir("nlp_tweets")
    tweet_times = []
    for f in ls:
        date_str = f.split()[0].split("-")
        date_time = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        tweet_times.append(date_time)
    return tweet_times
        

def poll_times():
    with open('trumpapproval.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            approval_times = []

            for row in reader:
                # print(row['startdate'] + "=>" + row['enddate'])
                startdate_str = row['startdate'].split("/")
                enddate_str = row['enddate'].split("/")

                start = datetime(int(startdate_str[2]), int(startdate_str[0]), int(startdate_str[1]))
                end = datetime(int(enddate_str[2]), int(enddate_str[0]), int(enddate_str[1]))
                approval_times.append({(start, end): (row['approve'], row['disapprove'])})
            return approval_times
                
def calculate_approval():
    tweet_times = approval()
    polls = poll_times()

    avgs = []

    for t_time in tweet_times:
        spanning_polls = []

        for p_time in polls:
            start = list(p_time.keys())[0][0]
            end = list(p_time.keys())[0][1]
            if start <= t_time <= end:
                spanning_polls.append(p_time)

        approve_str = map(lambda x: list(x.values())[0][0], spanning_polls)
        disapprove_str = map(lambda x: list(x.values())[0][1], spanning_polls)

        approve = map(lambda x: float(x), approve_str)
        disapprove = map(lambda x: float(x), disapprove_str)
        avgs.append({t_time: (round(mean(approve), 2), round(mean(disapprove), 2))})
    return avgs
        


if __name__ == "__main__":
    calculate_approval()