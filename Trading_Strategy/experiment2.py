import matplotlib.pyplot as plt
import StrategyLearner as sl
import pandas as pd
import marketsimcode as msc
from util import get_data
import datetime as dt
import random

def impact_effect():
    # impact=0
    df_0=compute_data()
    #print(df_0)
    
    # impact=0.0005
    df_1=compute_data(impact=0.0005)
    
    # impact=0.001
    df_2=compute_data(impact=0.001)
    
    # impact=0.005
    df_3=compute_data(impact=0.005)
    
    # impact=0.001
    df_4=compute_data(impact=0.01)
    
    # impact=0.05
    df_5=compute_data(impact=0.05)
    
    # plot chart
    plt.figure(4, figsize=(8,5))
    plt.title('How impact affect portfolio')
    plt.plot(df_0.index, df_0['portfolio'], label='impact=0', color='red')
    plt.plot(df_1.index, df_1['portfolio'], label='impact=0.0005', color='blue')
    plt.plot(df_2.index, df_2['portfolio'], label='impact=0.001', color='orange')
    plt.plot(df_3.index, df_3['portfolio'], label='impact=0.005', color='yellow')
    plt.plot(df_4.index, df_4['portfolio'], label='impact=0.01', color='black')
    plt.plot(df_5.index, df_5['portfolio'], label='impact=0.05', color='green')
    plt.xlabel('TIME')
    plt.ylabel('portfolio')
    plt.legend()
    #plt.show()
    plt.savefig('Experiment2')
    
    
    
def compute_data(symbol='JPM', \
    sd=dt.datetime(2008,1,1), \
    ed=dt.datetime(2009,12,31), \
    sv=100000, \
    impact=0, \
    commission=0):
    
    random.seed(100)
    learner=sl.StrategyLearner(impact=impact, commission=commission)
    learner.addEvidence(symbol=symbol, sd=sd, ed=ed, sv=sv)
    learner_trades=learner.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    #print(len(learner_trades))
    df_learner=msc.compute_portvals(df_orders=learner_trades, sd=sd, ed=ed, start_val=sv, commission=commission, impact=impact)
    df_learner['portfolio']=df_learner['portval']/df_learner['portval'][0]
    daily_ret=df_learner['portval'][1:]/df_learner['portval'].shift(1)-1
    std_dairet=daily_ret.std()
    cum_ret=df_learner['portfolio'][-1]-df_learner['portfolio'][0]
    sharpe_ratio=(252**0.5)*daily_ret.mean()/daily_ret.std()
    #print(sharpe_ratio)
    #print(cum_ret)
    #print(df_learner['portfolio'][-1])
    #print(std_dairet)
    return df_learner

def author():
    return 'whuang98'


if __name__=="__main__":
    impact_effect()