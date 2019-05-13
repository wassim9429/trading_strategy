
from __future__ import absolute_import
import numpy as np
import pandas as pd


def get_orders(positions, order_value=1000):
	"""
	Takes the output of the strategy (actions series which is pd Series)
	outputs a data frame  with 2 columns (order and shares)
	It works on just 1 symbol
	"""
	Orders = pd.DataFrame(columns=["Order","Shares"])
	holding = 0

	for index, position in positions.iteritems():
		if position == "long":
			if holding==0:
				Orders.loc[index] = ["BUY", int(order_value)]
			if holding==-order_value:
				Orders.loc[index] = ["BUY", int(order_value*2)]
			holding=order_value
		if position == "short":
			if holding==0:
				Orders.loc[index] = ["SELL", int(-order_value)]
			if holding==order_value:
				Orders.loc[index] = ["SELL", int(-order_value*2)]
			holding=-order_value
		if position == "close":
			if holding > 0:
				Orders.loc[index] = ["SELL", -holding]
			if holding < 0:
				Orders.loc[index] = ["BUY", -holding]
			holding=0
	return Orders



def compute_portvals(actions, data, order_value=1000, start_val = 1000, comission=0, impact=0):                                                                
    """
	Takes as input the 
	Orders: data frame with orders
	data: Prices data frame
	start_val: the start value

    """                                              
    Orders = get_orders(actions, order_value)
    Dates = Orders.index
    sd = actions.index.min()
    holdings = actions.replace(["long","short","close"], [order_value,-order_value,0]).multiply(data["Adj Close"])
    Impact = pd.Series([-impact]*Orders.shape[0], index = Orders.index)
    Impact = Impact.reindex(data.index, fill_value=0)
    Cash = -data["Adj Close"].multiply(Orders["Shares"], fill_value=0)
    Cash = Cash - Cash * comission + Impact
    Cash.loc[sd] = Cash.loc[sd] + start_val
    Cash = Cash.cumsum()
    portval = Cash + holdings
    portval = portval.dropna()
    return portval


def computing_daily_returns(port_val):
    daily_rets = port_val / port_val.shift(1) -1
    #daily_rets = daily_rets[1:] 
    return daily_rets


def compute_statistics(port_val):
    cr=(port_val.iloc[-1]/port_val.iloc[1]) - 1
    daily_rets = computing_daily_returns(port_val)
    adr=daily_rets.mean()
    sddr=daily_rets.std()  
    sr = np.sqrt(252) * adr / sddr
    return cr , adr, sddr, sr


def fill_for_noncomputable_vals(input_data, result_data):
    non_computable_values = np.repeat(
        np.nan, len(input_data) - len(result_data)
        )
    filled_result_data = np.append(non_computable_values, result_data)
    return filled_result_data


