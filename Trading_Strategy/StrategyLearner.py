"""  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
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
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
import datetime as dt  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
import pandas as pd  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
import util as ut  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
import random
import matplotlib.pyplot as plt
from indicators import *
import QLearner as ql
import marketsimcode as msc
 		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
class StrategyLearner(object):  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    # constructor  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    def __init__(self, verbose = False, impact=0.005, commission=9.95):  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        self.verbose = verbose  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        self.impact = impact  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        self.commission = commission 
        self.qlearning=ql.QLearner(num_states=10000, num_actions=3)
         		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    # this method should create a QLearner, and train it for trading  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        # add your code to do learning here  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        # example usage of the old backward compatible util function  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        syms=[symbol]
         		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        dates = pd.date_range(sd, ed)
          		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
          		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        prices = prices_all[syms]  # only portfolio symbols
          		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later 
         		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        if self.verbose: print(prices)  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
         	   		     			 
        #get features
        df_features=self.get_features(prices)
        #df_features=df_features.loc[sd:]
        
        #discretize the features
        df_features=self.discretize(df_features)
        
         		 			     			  	  		 	  	 		 			  		  			
        '''# example use with new colname  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        volume = volume_all[syms]  # only portfolio symbols  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        if self.verbose: print(volume) '''

        #train q learner
        normed_prices=prices/prices.iloc[0,0]
        holdings=0
        convergence=False
        a=0
        df_orders1=pd.DataFrame([0], columns=[symbol])
        
        while (not convergence) and (a<300):
            order=[]
            a+=1
            for i in range(normed_prices.shape[0]):
                if i==0:
                    reward=0
                    action=0
                else:
                    if normed_prices.index[i-1] in dict(order):
                        reward=holdings*(normed_prices.iloc[i,0]/(normed_prices.iloc[i-1,0]*(1+self.impact))-1)
                    else:
                        reward=holdings*(normed_prices.iloc[i,0]/normed_prices.iloc[i-1,0]-1)
                    
                    #reward=holdings*(normed_prices.iloc[i,0]/normed_prices.iloc[i-1,0]-1)*(1-self.impact)
                    state=df_features.iloc[i,4]
                    action=self.qlearning.query(state, reward)
                    #action=0 : CASH; action=1 : LONG; action=2 : SHORT
                
                if action==1: 
                    if holdings==0:
                        trade=1000
                        holdings=1000
                        date=normed_prices.index[i]
                        order.append((date,trade))
                    elif holdings==-1000:
                            trade=2000
                            holdings=1000
                            date=normed_prices.index[i]
                            order.append((date,trade))
                elif action==2:
                    if holdings==0:
                        trade=-1000
                        holdings=-1000
                        date=normed_prices.index[i]
                        order.append((date,trade))
                    elif holdings==1000:
                        trade=-2000
                        holdings=-1000
                        date=normed_prices.index[i]
                        order.append((date,trade))    
            
                
            df_orders=pd.DataFrame(order, columns=['date', symbol])
            df_orders.set_index('date', inplace=True)
            if df_orders.equals(df_orders1):
                convergence=True
            df_orders1=df_orders.copy()
        #print(df_orders)
        return df_orders
                 		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    # this method should use the existing policy and test it against new data  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 10000):  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        # here we build a fake set of trades  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        # your code should return the same sort of data
        #sd_query=sd-dt.timedelta(60)  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        dates = pd.date_range(sd, ed)
        	  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        trades = prices_all[[symbol,]]  # only portfolio symbols          		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later

        df_features=self.discretize(self.get_features(trades))
        #print(df_features)
        #df_features=df_features.loc[sd:]
        #print(trades) 
        normed_prices=trades/trades.iloc[0,0]
        holdings=0
        
        order=[]
        
        for i in range(normed_prices.shape[0]):
            if i==0:
                reward=0
                action=0
            else:
                
                state=df_features.iloc[i,4]
                action=self.qlearning.querysetstate(state)
                #action=0 : CASH; action=1 : LONG; action=2 : SHORT
                
                if action==1: 
                    if holdings==0:
                        trade=1000
                        holdings=1000
                        date=normed_prices.index[i]
                        order.append((date,trade))
                    elif holdings==-1000:
                        trade=2000
                        holdings=1000
                        date=normed_prices.index[i]
                        order.append((date,trade))
                elif action==2:
                    if holdings==0:
                        trade=-1000
                        holdings=-1000
                        date=normed_prices.index[i]
                        order.append((date,trade))
                    elif holdings==1000:
                        trade=-2000
                        holdings=-1000
                        date=normed_prices.index[i]
                        order.append((date,trade))
            
                        
        df_orders=pd.DataFrame(order, columns=['date', symbol])
        df_orders.set_index('date', inplace=True)
        
        #print(df_orders) 		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        	     			  		 			     			  	  		 	  	 		 			  		  			
        if self.verbose: print(type(trades)) # it better be a DataFrame!  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        if self.verbose: print(trades)  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        if self.verbose: print(prices_all)  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        return df_orders

    def author(self):
        return 'whuang98'
    
    
    def get_features(self, prices):
        p_sma=price_SMA(prices)
        #print(p_sma)
        BB_value=bollinger_bands(prices)
        ema_20=EMA(prices)
        ema_50=EMA(prices,win=50)
        ema_cross=ema_20.sub(ema_50)
        #print(ema_delta)
        force_index=Force_index(prices, win=20)
        df_features=pd.concat([p_sma,BB_value, ema_cross, force_index],axis=1)
        #print(df_features)
        return df_features


    def discretize(self, df_features):
        name=df_features.columns.values[2]
        bins_number=[0,1,2,3,4,5,6,7,8,9]
        di_sma, bins_sma=pd.cut(df_features['price/sma'], 10, retbins=True, labels=bins_number)
        #print(bins_sma)
        #print(di_sma)
        di_bb, bins_bb=pd.cut(df_features['bb'],10,retbins=True, labels=bins_number)
        di_emaCross, bins_emaCross=pd.cut(df_features[name],10,retbins=True,labels=bins_number)
        di_forceIndex, bins_forceIndex=pd.cut(df_features['roll-force-index'],10,retbins=True, labels=bins_number)
        '''df=di_bb.to_frame()
        plt.figure(1,figsize=(8,5))
        plt.plot(df.index, df)
        plt.show()'''
        df_features['states']=1000*di_sma.astype('int32')+100*di_bb.astype('int32')+10*di_emaCross.astype('int32')+di_forceIndex.astype('int32')
        
        return df_features

 		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
 		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
if __name__=="__main__":
    s=StrategyLearner()
    s.addEvidence()
    s.testPolicy()	  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    print("One does not simply think up a strategy")  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
