import pandas as pd
import numpy as np 	
import technical_indicators as TI
import function_helper as fh
import QLearner as ql
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
	actions = pd.Series(index = df.index, name = 'RSI_actions')
	actions.loc[df["relative_strength_index"]>70] = "short"
	actions.loc[df["relative_strength_index"]<30] = "long"
	actions = actions.fillna(method='ffill')
	return actions


def DT_strategy(data):
	return


def discretize(indicator, n_bins = 5):
  thresholds = np.linspace(0, 1, n_bins)
  quantiles = indicator.quantile(thresholds)
  return np.digitize(indicator, quantiles.values) -1


def discretizing_indicators(indicators_status):
	indicators_status["Momentum"] = discretize(indicators_status["Momentum"])
	indicators_status["Price_SMA_ratio"] = discretize(indicators_status["Price_SMA_ratio"])
	indicators_status["relative_strength_index"] = discretize(indicators_status["relative_strength_index"])
	# indicators_status["Stochastic_oscillator"] = discretize(indicators_status["Stochastic_oscillator"])
	# indicators_status["Bandwidth"] = discretize(indicators_status["Bandwidth"])
	return indicators_status


def index2state(s_index,n):
  s0 = s_index / (n**3)
  s1 = (s_index % (n**3)) / (n**2)
  s2 = (s_index % (n**2)) / n
  s3 = s_index%n
  return (s0, s1, s2, s3)

def trade_from_action(action, holding):
  if action == 0:
    # nothing
    return 0
  if action == 1:
    # long
    if holding == 1000:
      return 0 
    return 1000 - holding
  if action == 2:
    # short
    if holding == -1000:
      return 0
    return -1000 - holding

def state2index(state,n):
  # state a tuple of 4 (holding, ind1, ind2, ind3)
  # retrun index of state
  s_index = state[0] * n**3 + state[1] * n**2 + state[2] * n + state[3]
  return s_index

def position(holding):
  if holding==0:
    return 0
  if holding==1000:
    return 1
  if holding==-1000:
    return 2

def compare(x,y):
  return (x-y).sum()

class StrategyLearner(object):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # constructor  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False, impact=0.0, lookback=25, n_bins=5):  		   	  			    		  		  		    	 		 		   		 		  
        self.verbose = verbose
        # define   		   	  			    		  		  		    	 		 		   		 		  
        self.impact = impact
        self.n = n_bins
        num_states = 3 * self.n**3
        num_actions = 3
        self.lookback = lookback
        self.learner = ql.QLearner(num_states=num_states,\
            num_actions = num_actions, \
            alpha = 0.2, \
            gamma = 0.9, \
            rar = 0.3, \
            radr = 0.99, \
            dyna = 100, \
            verbose=False) #initialize the learner 
  		   	  			    		  		  		    	 		 		   		 		  
    # this method should create a QLearner, and train it for trading  		   	  			    		  		  		    	 		 		   		 		  
    def addEvidence(self, data):  		   	  			    		  		  		    	 		 		   		 		  
		n_bins = self.n  		   	  			    		  		  		    	 		 		   		 		  
		# Importing Technical indicators         
		T = TI.indicators_status(data, n=20)
		# Discretizing the indicators 
		indicators_df = discretizing_indicators(T) 
		# initializing the iteration counter
		iteration = 0
		# initializing convergence
		converged = False 
		# Learning QLearning        
		while((iteration <= 70) & (not converged)):
			print "iteration "
			print iteration
			# initializing holding
			iteration = iteration + 1
			# initializing holding
			holding = 0
			# initializing actions series
			actions = pd.Series(index = indicators_df.index)
			# initializing trades ( trade table)
			trades = pd.Series([0] * indicators_df.shape[0],index = indicators_df.index)
			# initilizing previous trades series
			prev_trades = trades.copy()
			# get the first row (information from first day)
			row = indicators_df.iloc[0]
			# compute first state
			state = (position(holding), row["Momentum"], row["Price_SMA_ratio"], row["relative_strength_index"])      
			# converting state to state index
			s_index = state2index(state,n_bins)
			# getting first action
			action = self.learner.querysetstate(s_index)
			# computing trade from action and holding
			trade = trade_from_action(action, holding)
			# adding trade to trade table
			trades[row.name] = trade
			if action == 1:
				actions[row.name] = "long"
			if action == 2:
				actions[row.name] = "short"
	      
			# looping through the train period
			for i in range(1, indicators_df.shape[0]):
				row = indicators_df.iloc[i]
				# computing new holding
				holding = holding + trade
				# computing reward
				reward = row["daily_returns"] * holding 
				# computing new state and new state index
				state = (position(holding), row["Momentum"], row["Price_SMA_ratio"], row["relative_strength_index"])
				
				s_index = state2index(state,n_bins)
				# getting new action and updating Qtable
				
				action = self.learner.query(s_index, reward)
				# getting trade from action
				trade = trade_from_action(action, holding)
				# updating trades table
				trades[row.name] = trade
				
				if action == 1:
					actions[row.name] = "long"
				if action == 2:
					actions[row.name] = "short"

			if compare(trades, prev_trades)==0 :
				print " \n\n it has converged \n\n"
				print trades
				print prev_trades
				converged = True
			

        
		actions = actions.fillna(method='ffill')

		return actions 

    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		   	  			    		  		  		    	 		 		   		 		  
    def testPolicy(self, data): 		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
		# Importing Technical indicators         
		T = TI.indicators_status(data, n=20)
		# Discretizing the indicators 
		indicators_df = discretizing_indicators(T) 
		n_bins = self.n

		holding = 0
		# initializing actions series
		actions = pd.Series(index = indicators_df.index)
		# initializing trades ( trade table)
		trades = pd.Series(index = indicators_df.index)
		# initilizing previous trades series
		prev_trades = trades.copy()
		# get the first row (information from first day)
		row = indicators_df.iloc[0]
		# compute first state
		state = (position(holding), row["Momentum"], row["Price_SMA_ratio"], row["relative_strength_index"])      
		# converting state to state index
		s_index = state2index(state,n_bins)
		# getting first action
		action = self.learner.querysetstate(s_index)
		# computing trade from action and holding
		trade = trade_from_action(action, holding)
		# adding trade to trade table
		trades[row.name] = trade
		if action == 1:
			actions[row.name] = "long"
		if action == 2:
			actions[row.name] = "short"


		for i in range(1, indicators_df.shape[0]):
			holding = holding + trade
			row = indicators_df.iloc[i]
			state = (position(holding), row["Momentum"], row["Price_SMA_ratio"], row["relative_strength_index"]) 
			s_index = state2index(state,n_bins)
			action = self.learner.querysetstate(s_index)
			trade = trade_from_action(action, holding)
			trades[i] = trade
			if action == 1:
				actions[row.name] = "long"
			if action == 2:
				actions[row.name] = "short"


		actions = actions.fillna(method='ffill') 	  			    		  		  		    	 		 		   		 		  
		return actions
