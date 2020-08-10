"""  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
Template for implementing QLearner  (c) 2015 Tucker Balch  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
Atlanta, Georgia 30332  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
All Rights Reserved  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
Template code for CS 4646/7646  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
works, including solutions to the projects assigned in this course. Students  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
and other users of this template code are advised not to share it with others  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
or to make it available on publicly viewable websites including repositories  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
such as github and gitlab.  This copyright statement should not be removed  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
or edited.  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
We do grant permission to share solutions privately with non-students such  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
as potential employers. However, sharing with other current or future  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
GT honor code violation.  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
-----do not edit anything above this line---  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
Student Name: Tucker Balch (replace with your name)  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
GT User ID: whuang98 (replace with your User ID)  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
GT ID: 903110269 (replace with your GT ID)  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
"""  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
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
        self.num_states=num_states  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        self.s = 0  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        self.a = 0
        self.alpha=alpha
        self.gamma=gamma
        self.verbose=verbose
        self.rar=rar
        self.radr=radr
        self.dyna=dyna
        self.experi=[]
        #print(self.experi.shape[0])
        self.Q=np.zeros((self.num_states,self.num_actions))
        #print(self.Q)
        
    def run_dyna(self):
        
        for i in range(self.dyna):
            #randn_halu=rand.randrange(0, self.experi.shape[0], 4)
            randn_halu=rand.randrange(len(self.experi))
            #s_halu=int(self.experi[randn_halu])
            row=self.experi[randn_halu]
            s_halu=row[0]
            #a_halu=int(self.experi[randn_halu+1])
            a_halu=row[1]
            #s_prime_halu=int(self.experi[randn_halu+2])
            s_prime_halu=row[2]
            r_halu=row[3]
            #print(r_halu)
            self.Q[s_halu, a_halu]=(1-self.alpha)*self.Q[s_halu,a_halu]+self.alpha*(r_halu+self.gamma*self.Q[s_prime_halu, np.argmax(self.Q[s_prime_halu,:])])  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    def querysetstate(self, s):  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        """  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        @summary: Update the state without updating the Q-table  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        @param s: The new state  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        @returns: The selected action  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        """  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        self.s = s
        ran_num=rand.random()
        #print(ran_num)
        if ran_num<self.rar:  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
            action = rand.randrange(0, self.num_actions)
        else:
            action = np.argmax(self.Q[s])
        		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        if self.verbose: print(f"s = {s}, a = {action}")
          		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        return action  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    def query(self,s_prime,r):  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        """  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        @summary: Update the Q table and return an action  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        @param s_prime: The new state  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        @param r: The reward  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        @returns: The selected action  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        """ 
        #self.s=s_prime
        
        s=self.s
        a=self.a
        self.Q[s,a]=(1-self.alpha)*self.Q[s,a]+self.alpha*(r+self.gamma*self.Q[s_prime, np.argmax(self.Q[s_prime,:])])
        #self.experi=np.append(self.experi, [s,a,s_prime,r])
        self.experi.append([s,a,s_prime,r])
        #self.experi=np.append(self.experi, [10,1,11,-2])
        #print(self.experi.shape[0])
        
        ran_num=rand.random()
        
        if ran_num<self.rar:
            action= rand.randrange(0, self.num_actions)
        else:
            action = np.argmax(self.Q[s_prime])
        
        if self.dyna!=0:
            self.run_dyna()    
        
        self.rar=self.rar*self.radr
        self.a=action            
        self.s=s_prime
 		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        if self.verbose: print(f"s = {s_prime}, a = {action}, r={r}")  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        return self.a


    def author(self):
        return 'whuang98'

  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
if __name__=="__main__":
  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    print("Remember Q from Star Trek? Well, this isn't him")  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
