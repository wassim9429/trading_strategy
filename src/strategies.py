import pandas as pd
import numpy as np 	



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