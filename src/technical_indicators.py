import numpy as np 
import pandas as pd
import catch_errors





def simple_moving_average(data, n):
    """Calculate the moving average for the given data.
    
    :param data: pandas.DataFrame of prices data
    :param n: int number of periods to look back 
    :return: pandas.Series of moving averages
    """
    catch_errors.check_for_period_error(data, n)
    MA = pd.Series(data['Close'].rolling(n, min_periods=n).mean(), name='SMA_' + str(n))
    return MA


def exponential_moving_average(data, n):
    """
    Calculate the expenential  moving averge af the close price of a stock over n 
    :param data: pandas.DataFrame
    :param n: number of periods to look back
    :return: pandas.Series of exponential moving average
    """
    catch_errors.check_for_period_error(data, n)
    EMA = pd.Series(df['Adj Close'].ewm(span=n, min_periods=n).mean(), name='EMA_' + str(n))
    return EMA


def momentum(data, n):
    """
    Calculate the Momentum af the close price of a stock over n 
    :param data: pandas.DataFrame 
    :param n: 
    :return: pandas.DataFrame
    """
    catch_errors.check_for_period_error(data, n)
    Momentum = pd.Series(data['Adj Close'].diff(n), name='Momentum_' + str(n))
    return Momentum

def price_SMA_ratio(data, n):
	"""
	Calculate the price over SMA ratio
	:param data: pandas.DataFrame of prices data
    :param n: int number of periods to look back 
    :return: pandas.Series 

	"""
	catch_errors.check_for_period_error(data, n)
	SMA = simple_moving_average(data, n)
	ratio = data['Adj Close'] / SMA
	return ratio


def daily_returns(data):
	"""
	Calculate the daily returns
	"""
	daily_rets = pd.Series(data['Adj Close'].div(data['Adj Close'].shift(1))-1, name='daily_rets')
	return daily_rets


def relative_strength_index(data, lookback):
	"""
	Calculate the relative strength index 
	:param data: pandas.DataFrame of prices data
    :param lookback: int number of periods to look back 
    :return: pandas.Series 

	"""
	catch_errors.check_for_period_error(data, lookback)
	daily_rets = daily_returns(data)
	rsi_list=[np.nan] * lookback
	for day in range(lookback,data['Adj Close'].shape[0]):
		up_gain = daily_rets[day - lookback+1:day+1].where(daily_rets >= 0).sum()
		down_loss = -1 * daily_rets.iloc[day - lookback+1:day+1].where(daily_rets<0).sum()
		if down_loss == 0:
			rsi_list.append(100)
		else:
			rs = (up_gain / lookback) / (down_loss / lookback)
			rsi_list.append(100 - (100/(1+rs)))
	rsi = pd.Series(rsi_list, index = data.index)
	return rsi



def stochastic_oscillator(data, n):

    catch_errors.check_for_period_error(data, n)

    percent_k = [100 * (data['Adj Close'] - data['Adj Close'].rolling(n, min_periods=n).min()) / 
    	(data['Adj Close'].rolling(n, min_periods=n).max() - data['Adj Close'].rolling(n, min_periods=n).min())]


    return percent_k


def bollinger_bands(data, n, std_mult=2.0):
	catch_errors.check_for_period_error(data, n)

	sma = simple_moving_average(data, n)
	smstd = sma.rolling(n, min_periods=n).std()
	upper_bb = sma + std_mult * smstd
	lower_bb = sma - std_mult * smstd

	return lower_bb, sma, upper_bb





def bandwidth(data, n, std_mult=2.0):
    """
    Bandwidth.
    Formula:
    bw = u_bb - l_bb / m_bb
    """
    catch_errors.check_for_period_error(data, n)
    lower_bb, mid_bb, upper_bb = bollinger_bands(data, n, std_mult=std_mult)

    bandwidth = 100 * (upper_bb - lower_bb )/  mid_bb

    return bandwidth

