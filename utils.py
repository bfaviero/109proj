#%matplotlib inline

import requests
import StringIO
import zipfile
import numpy as np
import pandas as pd # pandas
import matplotlib.pyplot as plt # module for plotting
import datetime
from datetime import timedelta

def get_closest_dates_to_quarters(df):
    dates = []
    quarters = get_quarters()
    quarters = quarters.reset_index().set_index(['year', 'quarter', 'date']).index
    for year, quarter, date in quarters:
        row = df.loc[df.year == year]
        if not row:
            continue
        row = df.loc[df.index == date]
        if row:
            dates.append(row.index.values[0])
            continue
        i = 1
        while True:
            date1 = date + timedelta(days=i)
            date2 = date - timedelta(days=i)
            row1 = df.loc[df.index == date1]
            row2 = df.loc[df.index == date2]
            if row1:
                dates.append(row1.index.values[0])
                break
            if row2:
                dates.append(row2.index.values[0])
                break
            i+=1
            if i>10:
                break
    return dates

def merge_with_quarters(df):
    dates = {}
    for date in df.index.unique():
        values = get_closest_quarter_to_date(date).values
        if values[0] != 0:
            dates[date] = values

    quarter_df = pd.DataFrame(columns=['date', 'quarter', 'year'], data=dates.values()).set_index('date')
    df2 = df.merge(quarter_df, left_index=True, right_index=True, how='left')
    return df2

def get_quarters():
    data = []
    for year in xrange(1999, 2014):
        i = 1
        for month, day in zip((3, 6, 9, 12), (31, 30, 30, 31)):
            date = datetime.date(year, month, day)
            data.append((date, i, year))
            i+=1
    df = pd.DataFrame(columns=['date', 'quarter', 'year'], data=data).set_index('date')
    return df


def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)

@memoize
def get_closest_quarter_to_date(date):
    def process_row(row):
        return pd.Series({'date': date, 'quarter':row.values[0][0], 'year': row.values[0][1]})
    quarters = get_quarters()
    row = quarters.loc[quarters.index == date]
    if row:
        return process_row(row)
    i = 1
    while True:
        date1 = date + timedelta(days=i)
        date2 = date - timedelta(days=i)
        row1 = quarters.loc[quarters.index == date1]
        row2 = quarters.loc[quarters.index == date2]
        if row1:
            return process_row(row1)
        if row2:
            return process_row(row2)
        i+=1
        if i>10:
            return pd.Series({'date':0, 'quarter':0, 'year': 0})

def get_quarter_info(df):
    #NOT USED ANYMORE
    quarters = get_quarters()
    quarters = quarters.loc[quarters.index >= datetime.date(1999, 12, 28)]
    dates = []
    for data in quarters.iterrows():
        date = data[0]
        l = get_closest_quarter_to_date(date)
        dates.append(l)
    df_quarters = pd.DataFrame(columns=['date', 'quarter', 'year'], data=dates)
    combined = pd.merge(df, df_quarters, on=['date']).sort(['date'])
    return combined