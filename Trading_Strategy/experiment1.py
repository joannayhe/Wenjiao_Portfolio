import matplotlib.pyplot as plt
import ManualStrategy as ms
import StrategyLearner as sl
import pandas as pd
import marketsimcode as msc
from util import get_data
import datetime as dt
import random


def compare():
    #manual trades
    manual_trades=ms.testPolicy()
    df_manual=msc.compute_portvals(df_orders=manual_trades)
    df_manual['portfolio']=df_manual['portval']/df_manual['portval'][0]
    #print(df_manual)
    
    # q learner trades
    random.seed(100)
    learner=sl.StrategyLearner()
    learner.addEvidence(symbol='JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000)
    learner_trades=learner.testPolicy(symbol='JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000)
    df_learner=msc.compute_portvals(df_orders=learner_trades)
    df_learner['portfolio']=df_learner['portval']/df_learner['portval'][0]
    print(df_learner['portfolio'][-1])
    #print(df_learner['portfolio'][-1]-df_learner['portfolio'][0])
    
    
    # benchmark
    sd=dt.datetime(2008,1,1)
    ed=dt.datetime(2009,12,31)
    df_benm=get_data(['JPM'], pd.date_range(sd, ed))
    df_benm.drop(['SPY'], axis=1, inplace=True)
    
    commission=9.95
    impact=0.005
    sv=100000
    cash_hold=sv-df_benm.iloc[0,0]*1000-commission-impact*1000*df_benm.iloc[0,0]
    df_benm['portval']=cash_hold+df_benm['JPM']*1000
    df_benm['portfolio']=df_benm['portval']/df_benm.iloc[0,1]
    
    # plot chart
    plt.figure(3, figsize=(8,5))
    plt.title('Portfolios of Trade Strategies')
    plt.plot(df_manual.index, df_manual['portfolio'], label='Manual Strategy', color='blue')
    plt.plot(df_learner.index, df_learner['portfolio'], label='Q learner Strategy', color='red')
    plt.plot(df_benm.index, df_benm['portfolio'],label='Benchmark', color='black')
    plt.xlabel('TIME')
    plt.ylabel('Portfolio')
    plt.legend()
    #plt.show()
    plt.savefig('Experiment1')
    


def author():
    return 'whuang98'


if __name__=="__main__":
    compare()