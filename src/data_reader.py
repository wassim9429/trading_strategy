import pandas as pd
from pandas_datareader import data

start_date = '2010-01-01'
end_date = '2016-12-31'

def get_data(index = 'GOOGL', start_date='2010-01-01', end_date = '2016-12-31' ):
	panel_data = data.DataReader(index, 'yahoo', start_date, end_date)
	return panel_data

def save_data(index = 'GOOGL', start_date='2010-01-01', end_date = '2016-12-31' ):
	panel_data = get_data(index, start_date, end_date)
	out_path= "data/" + index + ".csv"
	print panel_data
	panel_data.to_csv(out_path)
	

def import_data(index = 'GOOGL', start_date='2010-01-01', end_date = '2016-12-31' ):
	input_path= "data/" + index + ".csv"
	panel_data = pd.read_csv(input_path, index_col="Date")
	return panel_data
