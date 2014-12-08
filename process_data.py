#%matplotlib inline

import requests
import StringIO
import zipfile
import numpy as np
import pandas as pd # pandas
import matplotlib.pyplot as plt # module for plotting
import datetime
from datetime import timedelta
from utils import *

def get_returns(fund):
    fund = fund.replace('PRN', 'SH').replace('CALL', 'SH')
    fund_name = fund.filer.unique()[0]
    data = []
    for year in fund.year.unique():
        if np.isnan(year):
            continue
        for quarter in (1, 2, 3, 4):
            row = fund.loc[(fund.year == year) & (fund.quarter == quarter)]
            grouped = row.groupby('type')
            total_returns = 0
            for name, group in grouped:
                returns = 0
                returns = group.current_value.sum() - group.previous_value.sum()
                if name == 'PUT':
                    returns *= -1
                total_returns += returns
            data.append([year, quarter, total_returns])
    returns = pd.DataFrame(data=data, columns=['year', 'quarter', 'returns']).set_index(['year', 'quarter'])
    return returns

def get_sectors():
    df = pd.read_csv('data/ticker_sector.csv').set_index('ticker')
    return df

def get_funds():
    funds = []
    def parse_date(s):
            month, day, year = [int(i) for i in s.split('/')]
            if year >= 0 and year <=14:
                year += 2000
            else:
                year += 1900
            date = datetime.date(year, month, day)
            return date

    for i in range(1, 9):
        df = pd.read_csv('data/funds/fund'+str(i)+'.csv')
        date_index = list(df.columns).index('date')
        df['date'] = df.apply(lambda r: parse_date(r.values[date_index]), axis=1)
        # df = df.set_index('date')
        funds.append(df)
    return funds


def get_data(arg):
    cpi = pd.read_csv('data/metrics/'+arg+'.csv')
    def parse_date(s):
        month, day, year = [int(i) for i in s.split('/')]
        if year >= 0 and year <=14:
            year += 2000
        else:
            year += 1900
        date = datetime.date(year, month, day)
        return date

    cpi['date'] = cpi.apply(lambda r: parse_date(r.values[0]), axis=1)
    cpi = cpi.set_index('date')
    df = merge_with_quarters(cpi)
    dates = get_closest_dates_to_quarters(df)
    dates_df = pd.DataFrame(columns=['date'], data=dates).set_index('date')
    return df.merge(dates_df, left_index=True, right_index=True).set_index(['year', 'quarter'])

def get_cpi():
    return get_data('cpi')

def get_gdp():
    return get_data('gdp')

def get_jobless():
    return get_data('jobless')

def get_sentiment():
    return get_data('sentiment')

def get_index(index):
    dow = pd.read_csv('data/metrics/%s.csv' % index)
    def transform_date(d):
        s = str(d)
        year, month, day = map(int, [s[:4], s[4:6], s[6:]])
        return datetime.date(year, month, day)
    dow.date = [transform_date(date) for date in dow.date]
    dow = dow.set_index('date')
    df = merge_with_quarters(dow)
    dates = get_closest_dates_to_quarters(df)
    dates_df = pd.DataFrame(columns=['date'], data=dates).set_index('date')
    return df.merge(dates_df, left_index=True, right_index=True).set_index(['year', 'quarter'])[['adj_close']]

def get_dow():
    return get_index('dow')

def get_snp():
    return get_index('snp')

def get_index_daily(index):
    dow = pd.read_csv('data/metrics/%s.csv' % index)
    def transform_date(d):
        s = str(d)
        year, month, day = map(int, [s[:4], s[4:6], s[6:]])
        return datetime.date(year, month, day)
    dow.date = [transform_date(date) for date in dow.date]
    dow = dow.set_index('date')
    return dow

def get_inflation():
    inflation = pd.read_csv('data/metrics/inflation_monthly.csv')
    def transform_inflation(elt):
        try:
            return float(elt[:-1])/100.0
        except:
            return 999
    for i in range(1, len(inflation.columns)):
        col = inflation.columns[i]
        inflation[col] = inflation.apply(lambda r: transform_inflation(r.values[i]), axis=1)
    inflation.columns = ['YEAR', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    data = []
    for row in inflation.iterrows():
        row = row[1]
        year = int(row[0])
        for i in range(1, 13):
            inflation = row[i]
            date = datetime.date(year, i, 1)
            data.append([date, inflation])
    df = pd.DataFrame(columns=['date', 'inflation'], data=data).set_index('date')
    df = merge_with_quarters(df)
    dates = get_closest_dates_to_quarters(df)
    dates_df = pd.DataFrame(columns=['date'], data=dates).set_index('date')
    return df.merge(dates_df, left_index=True, right_index=True).set_index(['year', 'quarter'])[['inflation']]
