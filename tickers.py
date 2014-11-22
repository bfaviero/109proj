from yahoo_finance import Share
from dateutil.parser import parse
from datetime import timedelta
import datetime

class PriceData:
    def __init__(self, data):
        self.volume = int(data['Volume'])
        self.symbol = data['Symbol']
        self.adj_close = float(data['Adj_Close'])
        self.high = float(data['High'])
        self.low = float(data['Low'])
        self.date = parse(data['Date']).date()
        self.close = float(data['Close'])
        self.open = float(data['Open'])

def string_to_date(s):
        return parse(s).date()

def is_weekend(date):
        day = date.weekday()
        return day == 5 or date == 6

def add_one_day(date):
        return date + timedelta(days=1)

def remove_one_day(date):
        return date - timedelta(days=1)

def is_trading_day(stock, date):
        try:
            data = stock.get_historical(str(date), str(date))
            return data
        except TypeError:
            return False

def get_previous_trading_day(stock, date):
        while True:
            date = remove_one_day(date)
            data = is_trading_day(stock, date)
            if data:
                return data

def get_next_trading_day(stock, date):
        while True:
            date = add_one_day(date)
            data = is_trading_day(stock, date)
            if data:
                return data

def get_price_of_stock_on_day(stock, date, get_later_day):
    stock = Share(stock)
    data = is_trading_day(stock, date)
    if data:
        return data
    else:
        if get_later_day:
            return get_next_trading_day(stock, date)
        else:
            return get_previous_trading_day(stock, date)

def get_price_difference(stock, date1, date2):
    data1 = PriceData(get_price_of_stock_on_day(stock, date1, get_later_day=False))
    data2 = PriceData(get_price_of_stock_on_day(stock, date2, get_later_day=True))
    print data2.adj_close - data1.adj_close

def get_ytd(stock, date):
    date1 = datetime.date(date.year, 1, 1)
    data1 = PriceData(get_price_of_stock_on_day(stock, date1, get_later_day=True))
    data2 = PriceData(get_price_of_stock_on_day(stock, date, get_later_day=False))
    return data2.adj_close - data1.adj_close
