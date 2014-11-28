from datetime import timedelta
from process_data import *
from pydash import flatten
from pyq_api import get_ticker_info
from tickers import *
from utils import *
from yahoo_finance import Share
import datetime
import matplotlib.pyplot as plt # module for plotting
import numpy as np
import pandas as pd # pandas
import requests
import StringIO
import zipfile

#ticker, date, open, high, low, close, vol, adj_close
class PriceData:
    def __init__(self, data):

        self.symbol = data[0]
        self.date = float(data[1])
        self.open = float(data[2])
        self.high = float(data[3])
        self.low = float(data[4])
        self.close = float(data[5])
        self.volume = float(data[6])
        self.adj_close = float(data[7])

def string_to_date(s):
        return parse(s).date()

def _add_one_day(date):
        return date + timedelta(days=1)

def _remove_one_day(date):
        return date - timedelta(days=1)

def trading_data_on_date(stock, date):
        data = get_ticker_info(date, date, stock)
        if data:
            return PriceData(data[0])
        return data

def _get_previous_trading_data(stock, date):
        date = _remove_one_day(date)
        data = trading_data_on_date(stock, date)
        i = 0
        while not data:
            date = _remove_one_day(date)
            data = trading_data_on_date(stock, date)
            i+=1
            if i > 3:
                return None
        return data

def _get_next_trading_data(stock, date):
        date = _add_one_day(date)
        data = trading_data_on_date(stock, date)
        i = 0
        while not data:
            date = _add_one_day(date)
            data = trading_data_on_date(stock, date)
            i+=1
            if i > 3:
                return None
        return data



def get_data_of_stock_on_or_around_day(stock, date, get_later_day=False):
    data = trading_data_on_date(stock, date)
    if data:
        return data.adj_close
    else:
        if get_later_day:
            data = _get_next_trading_data(stock, date)
        else:
            data = _get_previous_trading_data(stock, date)
        return data if data else None


def get_price_of_stock_on_or_around_day(stock, date, get_later_day=False):
    data = get_data_of_stock_on_or_around_day(stock, date, get_later_day)
    return data.adj_close if data else NOne



def get_price_difference(stock, date1, date2):
    data1 = get_price_of_stock_on_or_around_day(stock, date1, get_later_day=False)
    data2 = get_price_of_stock_on_or_around_day(stock, date2, get_later_day=True)
    if not (data1 and data2):
        return None
    return data2 - data1

def get_ytd(stock, date):
    date1 = datetime.date(date.year, 1, 1)
    data1 = get_price_of_stock_on_or_around_day(stock, date1, get_later_day=True)
    data2 = get_price_of_stock_on_or_around_day(stock, date, get_later_day=False)
    if not (data1 and data2):
        return None
    return data2 - data1

def process_ticker_returns(ticker, array):
    columns = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close']
    df = pd.DataFrame(columns=columns, data=array).drop_duplicates()
    def transform_date(d):
        s = str(d)
        year, month, day = map(int, [s[:4], s[4:6], s[6:]])
        return datetime.date(year, month, day)
    df.date = [transform_date(date) for date in df.date]
    df = df.set_index('date').sort().drop_duplicates()
    unique_tickers = df.ticker.unique()
    dfs = [df.loc[df.ticker == tick] for tick in unique_tickers]
    for i, df in enumerate(dfs):
        df.ticker = ticker + str(i)
    return dfs

def get_price_of_stock_between_dates(ticker, date1, date2):
    data = get_ticker_info(date1, date2, ticker)
    if not data:
        return emptyFrame()
    return process_ticker_returns(ticker, data)

def get_price_of_stock_at_dates(ticker, dates):
    data = [get_ticker_info(date, date, ticker) for date in dates if date]
    data = flatten(data)
    if not data:
        return emptyFrame()
    return process_ticker_returns(ticker, data)

def get_price_of_stock_at_dates_flexible(ticker, dates):
    data = [get_data_of_stock_on_or_around_day(ticker, date) for date in dates if date]
    data = flatten(data)
    if not data:
        return emptyFrame()
    return process_ticker_returns(ticker, data)
