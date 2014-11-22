#%matplotlib inline

import requests
import StringIO
import zipfile
import numpy as np
import pandas as pd # pandas
import matplotlib.pyplot as plt # module for plotting
from dateutil.parser import parse

def get_cpi():
    cpi = pd.read_csv('data/metrics/cpi_monthly.csv')
    cpi['observation_date'] = cpi.apply(lambda r: parse(r.values[0]).date(), axis=1)
    cpi = cpi[['date', 'cpi']]
    return cpi

def get_dow():
    dow = pd.read_csv('data/metrics/dow_daily.csv')
    def transform_date(d):
        s = str(d)
        return parse('%s-%s-%s' % (s[:4], s[4:6], s[6:])).date()
    dow.date = [transform_date(date) for date in dow.date]
    return dow

def get_gdp():
    gdp = pd.read_csv('data/metrics/gdp_quarterly.csv')
    gdp['date'] = gdp.apply(lambda r: parse(r.values[0]).date(), axis=1)
    return gdp

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
    return inflation

def get_jobless():
    jobless = pd.read_csv('data/metrics/jobless_weekly.csv')
    jobless['observation_date'] = jobless.apply(lambda r: parse(r.values[0]).date(), axis=1)
    jobless.columns = ['date', 'jobless']
    return jobless

def get_snp():
    snp = pd.read_csv('data/metrics/s&p_daily.csv')
    def transform_date(d):
        s = str(d)
        return parse('%s-%s-%s' % (s[:4], s[4:6], s[6:])).date()
    snp.date = [transform_date(date) for date in snp.date]
    return snp

def get_sentiment():
    sentiment = pd.read_csv('data/metrics/jobless_weekly.csv')
    sentiment['observation_date'] = sentiment.apply(lambda r: parse(r.values[0]).date(), axis=1)
    sentiment.columns = ['date', 'sentiment']
    return sentiment

