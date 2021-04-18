import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pdb
import csv
from scipy.interpolate import make_interp_spline
from datetime import datetime
import numpy as np


def graph_approval():
    data = []
    with open('sentiments/sia.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            data.append(row)

    # sort data first
    datetimes = [x["date"] for x in data]
    dates = matplotlib.dates.date2num(datetimes)
    dates = sorted(dates)

    poss = [float(x["pos"]) for x in data]
    negs = [float(x["neg"]) for x in data]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot_date(dates, poss, 'b-', color="green")
    ax.set_ylim([0, 100])

    ax2 = fig.add_subplot(1, 1, 1)
    ax2.plot_date(dates, negs, 'b-', color="red")
    ax.set_ylim([0, 100])

    plt.axhline(y=50, color='grey', linestyle='-')
    plt.show()

def graph_sentiment():
    approval_data = []
    with open('approval/trump.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            approval_data.append(row)
    approval_data_sorted = sorted(approval_data, key = lambda row: datetime.strptime(row["date"].split()[0], "%Y-%m-%d"))


    sentiment_data = []
    with open('sentiments/fl.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            sentiment_data.append(row)
    sentiment_data_sorted = sorted(sentiment_data, key = lambda row: datetime.strptime(row["date"].split()[0], "%Y-%m-%d"))

    # pdb.set_trace()

    # sort data first
    approval_datetimes = [x["date"] for x in approval_data]
    approval_dates = matplotlib.dates.date2num(approval_datetimes)
    approval_dates = sorted(approval_dates)

    sentiment_datetimes = [x["date"] for x in sentiment_data]
    sentiment_dates = matplotlib.dates.date2num(sentiment_datetimes)
    sentiment_dates = sorted(sentiment_dates)

    # NORMALIZE SENTIMENT
    poss = [float(x["pos"]) + float(x["neu"]) / 2 for x in sentiment_data]
    neus = [float(x["neu"]) for x in sentiment_data]
    negs = [float(x["neg"]) + float(x["neu"]) / 2 for x in sentiment_data]
    sentiment_diff = [float(x["pos"]) - float(x["neg"]) for x in sentiment_data]

    # NORMALIZE APPROVAL
    poss = [float(x["pos"]) / 100 for x in approval_data]
    negs = [float(x["neg"]) / 100 for x in approval_data]
    approval_diff = [((float(x["pos"]) / 100) - (float(x["neg"])) / 100) for x in approval_data]

    # SMOOTHING
    xyspline = make_interp_spline(sentiment_dates, sentiment_diff)
    x_ = np.linspace(min(sentiment_dates), max(sentiment_dates), 36)
    y_ = xyspline(x_)

    xyspline2 = make_interp_spline(approval_dates, approval_diff)
    x_2 = np.linspace(min(approval_dates), max(approval_dates), 36)
    y_2 = xyspline2(x_2)

    # FIND CORRELATION
    # TODO - find correlation for differences!
    pdb.set_trace()
    print(np.corrcoef(y_, y_2))

    # GRAPHING
    fig = plt.figure()

    ax = fig.add_subplot(1, 1, 1)
    # ax.plot_date(x_2, y_2, 'b-', color="red")
    ax.plot_date(x_, y_, 'b-', color="blue")
    ax.set_ylim([-1, 1])

    ax = fig.add_subplot(1, 1, 1)
    # ax.plot_date(x_, y_, 'b-', color="green")
    ax.plot_date(x_2, y_2, 'b-', color="yellow")
    ax.set_ylim([-1, 1])

    # ax2 = fig.add_subplot(1, 1, 1)
    # ax2.plot_date(dates, negs, 'b-', color="red")
    # ax.set_ylim([0, 1])

    plt.axhline(y=0, color='grey', linestyle='-')
    plt.show()


if __name__ == "__main__":
    # graph_approval()
    graph_sentiment()