import Quandl

auth_token = "v2tx16u_kQotxDgQi_22"

def get_price_history(stock, start_time, end_time, interval):
	mydata = Quandl.get("WIKI/" + stock, trim_start=start_time, trim_end=end_time, collapse=interval, authtoken=auth_token)
	return mydata

def get_params(stock, params, start_time, end_time):
	params = map(lambda x: "DMDRN/" + stock + "_" + x, params)
	print params
	mydata = Quandl.get(params, trim_start=start_time, trim_end=end_time, authtoken=auth_token, collapse='quarterly')
	# tokens available:
	# returns="numpy"
	# collapse="annual" out of ("daily"|weekly"|"monthly"|"quarterly"|"annual")
	# rows=5
	# sort_order="asc" or "desc"
	# exclude_headers=true
	# column=<index num>
	# can also put all the query strings in a list 
	return mydata

def get_sec_raw(ticker, code, freq):
	# SEC/{STOCK TICKER}_{UPPERCASE SEC CODE}_{FREQUENCY}
	mydata = Quandl.get("SEC/" + ticker +"_"+code+"_" + freq, trim_start=start_time, trim_end=end_time, authtoken=auth_token)
	return mydata

def get_sec_tickers():
	url = "https://s3.amazonaws.com/quandl-static-content/Ticker+CSV%27s/secwiki_tickers.csv"
	return


def get_gdp(start_time, end_time):
	# monthly
	mydata = Quandl.get("FRED/GDP", trim_start=start_time, trim_end=end_time, authtoken=auth_token)
	return mydata

def get_cpi(start_time, end_time):
	# monthly
	mydata = Quandl.get("FRED/CPIAUCSL", trim_start=start_time, trim_end=end_time, authtoken=auth_token)
	return mydata

def get_unemployment(start_time, end_time):
	# monthly
	mydata = Quandl.get("FRED/UNRATE", trim_start=start_time, trim_end=end_time, authtoken=auth_token)
	return mydata

def get_industry(industry_name, source):
	datasets = Quandl.search(query = "crude oil", source = "DOE", page = 2, prints = True)
	return mydata

def get_exchange_rate(from_code, to_code):
	# For all codes, go to:
	# https://www.quandl.com/CURRFX
	# daily
	mydata = Quandl.get("CURRFX/"+from_code+to_code, authtoken=auth_token)
	return mydata

def get_commodity_data(code,start_time, end_time):
	# All codes are listed here:
	# daily info
	# https://www.quandl.com/help/api-for-commodity-data
	mydata = Quandl.get(code, trim_start=start_time, trim_end=end_time, authtoken=auth_token)
	return mydata

def get_sp_info():
	# if necessary, look into:
	# https://www.quandl.com/MULTPL

	#example getting index daily
	mydata = Quandl.get("YAHOO/INDEX_GSPC", trim_start=start_time, trim_end=end_time, authtoken=auth_token)
	return mydata

def test_get():
	# mydata = get_adj_closing_quotes('NSE', "OIL", "2000-01-01","2014-11-12")
	# mydata = get_cpi("2000-01-01","2014-09-30")
 	# mydata = get_commodity_data("WSJ/AU_ZAR", "2000-01-01","2014-09-30")
 	mydata = get_params("MSFT", ["MKT_CAP","PE_CURR"], "2000-01-01","2014-09-30")
	print mydata

# mydata = Quandl.get("NSE/OIL", authtoken=auth_token)

# data = Quandl.get('PRAGUESE/PX', authtoken='xxxxxx', trim_start='2001-01-01',
#                   trim_end='2010-01-01', collapse='annual',
#                   transformation='rdiff', rows=4, returns='numpy')