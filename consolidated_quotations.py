#!/bin/python

import pandas as pd
import numpy as np
import datetime
import yaml

from pandas_datareader import data as web

end = datetime.date.today()
start = end - datetime.timedelta(365)

table = web.DataReader("PETR4.SA", "yahoo", start, end)
table = table[table.Volume != 0]
table = table[["Adj Close"]]
table.rename(columns={'Adj Close': "PETR4.SA"}, inplace=True)

if __name__ == '__main__':
    with open("config.yaml") as fh:
        config = yaml.load(fh)

    for code in config.get("codes"):
        table2 = web.DataReader(code, "yahoo", start, end)
        table2 = table2[table2.Volume != 0]
        table2 = table2[["Adj Close"]]
        table2.rename(columns={'Adj Close': code}, inplace=True)

        table = pd.concat([table, table2], axis=1)

    table.to_csv("~/all.csv")
