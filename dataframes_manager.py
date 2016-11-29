
import pandas as pd
import numpy as np
import datetime
import yaml

import pandas.io.data as web
#from pandas_datareader import data as web

class DataFrameManager():
    def set_table(equity):
        end = datetime.date.today()
        start = end - datetime.timedelta(days=30)

        try:
            try:
                table = web.DataReader(equity, "yahoo", start, end)
            except:
                table = web.DataReader(equity, "google", start, end)

            table = table[table.Volume != 0].tail(14)
        except:
            return False

        return table
