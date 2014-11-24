from pyq_api import get_ticker_info
from yahoo_finance import Share
from dateutil.parser import parse
from datetime import timedelta
import datetime

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

def is_weekend(date):
        day = date.weekday()
        return day == 5 or date == 6

def add_one_day(date):
        return date + timedelta(days=1)

def remove_one_day(date):
        return date - timedelta(days=1)

def trading_data_on_date(stock, date):
        data = get_ticker_info(date, date, [stock])[0]
        if data:
            return PriceData(data)
        return data

def get_previous_trading_data(stock, date):
        while True:
            date = remove_one_day(date)
            data = is_trading_day(stock, date)
            return data

def get_next_trading_data(stock, date):
        while True:
            date = add_one_day(date)
            data = is_trading_day(stock, date)
            return data

def get_price_of_stock_on_or_around_day(stock, date, get_later_day=False):
    data = trading_data_on_date(stock, date)
    if data:
        return data
    else:
        if get_later_day:
            return get_next_trading_data(stock, date)
        else:
            return get_previous_trading_data(stock, date)

def get_price_difference(stock, date1, date2):
    data1 = get_price_of_stock_on_or_around_day(stock, date1, get_later_day=False)
    data2 = get_price_of_stock_on_or_around_day(stock, date2, get_later_day=True)
    print data2.adj_close - data1.adj_close

def get_ytd(stock, date):
    date1 = datetime.date(date.year, 1, 1)
    data1 = get_price_of_stock_on_or_around_day(stock, date1, get_later_day=True)
    data2 = get_price_of_stock_on_or_around_day(stock, date, get_later_day=False)
    return data2.adj_close - data1.adj_close

#date = string_to_date('2014-4-22')
#print get_price_of_stock_on_or_around_day('GOOG', date, get_later_day=True).adj_close