#! /bin/python

import pandas as pd
import numpy as np
import pandas.io.data as web
import datetime

def generate_analisys():
    equitys = ["RAPT4.SA", "MRFG3.SA", "USIM5.SA", "TIMP3.SA", "RUMO3.SA",
               "POMO4.SA", "ITSA4.SA", "GOLL4.SA", "GOAU4.SA", "GFSA3.SA",
               "EVEN3.SA", "ELPL4.SA", "ECOR3.SA", "DTEX3.SA", "CYRE3.SA",
               "CMIG4.SA", "BRPR3.SA"]

    for i in equitys:
        print(i)
        print(define_ifr(set_table(i)))

def set_table(equity):
    end = datetime.date.today()
    start = end - datetime.timedelta(days=30)
    table = web.DataReader(equity, "yahoo", start, end)
    table = table[table.Volume != 0].tail(14)
    return table

def define_ifr(table):
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

    earnings_average = np.sum(np.array(earnings))/14
    losses_average = np.sum(np.array(losses))/14
    relative_force = earnings_average / losses_average
    return 100 - (100/(1+relative_force))

generate_analisys()
