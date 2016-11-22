#!/bin/python

import pandas as pd
import numpy as np
import datetime
import yaml

from pandas_datareader import data as web


def generate_analisys(code):
    return define_ifr(set_table(code))


def set_table(equity):
    end = datetime.date.today()
    start = end - datetime.timedelta(days=30)

    try:
        table = web.DataReader(equity, "yahoo", start, end)
        table = table[table.Volume != 0].tail(14)
    except:
        return False

    return table


def define_ifr(table):
    if isinstance(table, pd.core.frame.DataFrame):

        d0 = None
        d1 = None
        earnings = []
        losses = []

        for index, row in table.iterrows():
            d1 = row["Close"]

            if d0 == None:
                d0 = d1
            elif d0 > d1:
                earnings.append(abs(d0-d1))
                d0 = d1
            elif d0 < d1:
                losses.append(abs(d0-d1))
                d0 = d1

        earnings_average = np.sum(np.array(earnings)) / 14
        losses_average = np.sum(np.array(losses)) / 14
        relative_force = earnings_average / losses_average
        return 100 - (100 / (1 + relative_force))


if __name__ == '__main__':
    with open("config.yaml") as fh:
        config = yaml.load(fh)

    for code in config.get("codes"):
        print("{0} => {1}".format(code, generate_analisys(code)))
