import pandas as pd
import numpy as np 	
import technical_indicators as TI
import function_helper as fh

def benchmark(data):
	sd = data.index.min()
	ed = data.index.max()
	# buy 1000 shares in sd
	actions = pd.Series(["long"]*data.shape[0],name="benchmark_actions", index=data.index)
	actions.loc[ed] = "close"
	return actions



def optimal_strategy(data):
	tomorrow = data["Adj Close"].shift(-1)
	actions = pd.Series(np.where(tomorrow >= data["Adj Close"], "long", "short"), name="benchmark_actions", index=data.index) 
	ed = data.index.max()
	actions.loc[ed] = "close"
	return actions

def manual_strategy(data):
	df = TI.indicators_status(data, n=20)
	print df["relative_strength_index"].min()
	print df["relative_strength_index"].max()
	actions = pd.Series(index = df.index, name = 'RSI_actions')
	actions.loc[df["relative_strength_index"]>70] = "short"
	actions.loc[df["relative_strength_index"]<30] = "long"
	print actions


def DT_strategy(data):
	return

def RL_strategy(data):
	return

def discretize(indicator, n_bins = 5):
  thresholds = np.linspace(0, 1, n_bins)
  quantiles = indicator.quantile(thresholds)
  return np.digitize(indicator, quantiles.values) -1


def discretizing_indicators(indicators_status):
	indicators_status["Momentum"] = discretize(indicators_status["Momentum"])
	indicators_status["Price_SMA_ratio"] = discretize(indicators_status["Price_SMA_ratio"])
	indicators_status["relative_strength_index"] = discretize(indicators_status["relative_strength_index"])
	indicators_status["Stochastic_oscillator"] = discretize(indicators_status["Stochastic_oscillator"])
	indicators_status["Bandwidth"] = discretize(indicators_status["Bandwidth"])
	print indicators_status



