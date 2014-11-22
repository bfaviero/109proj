#%matplotlib inline

import requests
import StringIO
import zipfile
import numpy as np
import pandas as pd # pandas
import matplotlib.pyplot as plt # module for plotting
from dateutil.parser import parse

funds = []
for i in range(1, 9):
    fund = pd.read_csv('data/funds/fund'+str(i)+'.csv')
    fund['date'] = fund.apply(lambda r: parse(r.values[3]).date(), axis=1)
    funds.append(fund)
