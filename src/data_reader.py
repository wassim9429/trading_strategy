import pandas as pd
from pandas_datareader import data

start_date = '2010-01-01'
end_date = '2016-12-31'


panel_data = data.DataReader('INPX', 'yahoo', start_date, end_date)
print panel_data