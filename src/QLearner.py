import numpy as np                                                                                                
import random as rand



class QLearner(object):                                                                                               
                                                                                              
    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):                                                                                             
                                                                                              
        self.verbose = verbose                                                                                                
        self.num_actions = num_actions
        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma                                                                                                
        self.s = 0                                                                                                
        self.a = 0
        self.rar= rar
        self.radr = radr
        # initialize Q
        self.Q = np.zeros(shape=(self.num_states, self.num_actions), dtype=float) 
        self.dyna = dyna
        if self.dyna > 0:
            self.tuples = []
            
                                                                                              
    def querysetstate(self, s):                                                                                               
        """                                                                                               
        @summary: Update the state without updating the Q-table                                                                                               
        @param s: The new state                                                                                               
        @returns: The selected action                                                                                             
        """                                                                                               
        self.s = int(s)
                                                                                                             
        action = np.argmax(self.Q[s])
        if self.verbose: print "s =", s,"a =",action
        self.a = int(action)                                                                                            
        return int(action) 
                                                                      
                                                                                              
    def query(self,s_prime,r):                                                                                                
        """                                                                                               
        @summary: Update the Q table and return an action                                                                                             
        @param s_prime: The new state                                                                                             
        @param r: The new reward                                                                                              
        @returns: The selected action                                                                                             
        """
        # update Q

        best_future_action = np.argmax(self.Q[s_prime])
        reward = (1 - self.alpha) * self.Q[self.s, self.a] + self.alpha * (r + self.gamma * self.Q[s_prime,best_future_action])

        self.Q[int(self.s) , int(self.a)] = reward

       
        # Run Dyna ----------------
        if (self.dyna > 0):
            # update immediate reward
            self.tuples.append((self.s, self.a, int(s_prime), r))

            for k in range(self.dyna):
                # get random old experience
                (state, action, s_p, r) = rand.choice(self.tuples)
                best_future_action = np.argmax(self.Q[s_p])
                reward = (1 - self.alpha) * self.Q[state, action] + self.alpha * (r + self.gamma * self.Q[s_p,best_future_action])
                # update Q
                self.Q[state, action] = reward


        # get new best action and upadting a and s in self
        self.s = int(s_prime)
        prob = np.random.random(1)[0]
        if prob <= self.rar:                                                                                                  
            action = rand.randint(0, self.num_actions-1)                                                                                                      
        else:
            action = np.argmax(self.Q[s_prime])
        if self.verbose: print "s =", s_prime,"a =",action
        self.a = int(action)
        # update random factor
        self.rar= self.rar * self.radr

        if self.verbose: print "s =", s_prime,"a =",action ,"r =",r                                                                                             
        return action                                                                                             
                                                                                              
if __name__=="__main__":                                                                                              
    print "QLearning class"   