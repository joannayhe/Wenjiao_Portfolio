import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from indicators import *
from util import get_data
from marketsimcode import compute_portvals


def testPolicy(symbol='JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000):

    normed_price=get_df(symbol,sd,ed)
    p_sma=price_SMA(normed_price)
    #print(p_sma)
    BB_value=bollinger_bands(normed_price)
    #print(BB_value)
    ema_20=EMA(normed_price)
    #print(ema_20)
    ema_50=EMA(normed_price,win=50)
    #print(ema_50)
    force_index=Force_index(normed_price, win=20)
    #print(force_index)
    
    position=0 # when short, position=-1; when long, position=1
    order=[]
    
    for i in range(normed_price.shape[0]):
        if (p_sma.iloc[i,0]<0.93) or (BB_value.iloc[i,0]<0 and ema_20.iloc[i,0]>ema_50.iloc[i,0] and force_index.iloc[i,0]>0):
            if position==0:
                trade=1000
                position=1
                date=normed_price.index[i]
                order.append((date,trade))
            elif position==-1:
                trade=2000
                position=1
                date=normed_price.index[i]
                order.append((date,trade))
        
        elif (p_sma.iloc[i,0]>1.08) or (BB_value.iloc[i,0]>1 and ema_20.iloc[i,0]<ema_50.iloc[i,0] and force_index.iloc[i,0]<0): 
            if position==0:
                trade=-1000
                position=-1
                date=normed_price.index[i]
                order.append((date,trade))
            elif position==1:
                trade=-2000
                position=-1
                date=normed_price.index[i]
                order.append((date,trade))
                
    df_orders=pd.DataFrame(order, columns=['date', symbol])
    df_orders.set_index('date', inplace=True)
    #print(df_orders)
    return df_orders            
    

def plot_data(symbol='JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000,n=1):
    # benchmark
    df_benm=get_data([symbol], pd.date_range(sd, ed))
    if symbol!='SPY':
        df_benm.drop(['SPY'], axis=1, inplace=True)
    
    commission=9.95
    impact=0.005
    cash_hold=sv-df_benm.iloc[0,0]*1000-commission-impact*1000*df_benm.iloc[0,0]
    df_benm['portval']=cash_hold+df_benm[symbol]*1000
    df_benm['portfolio']=df_benm['portval']/df_benm.iloc[0,1]
    #print(df_benm)
    
    # manual strategy
    df_orders=testPolicy(sd=sd, ed=ed) 
    df_manual=compute_portvals(df_orders=df_orders, sd=sd, ed=ed)
    df_manual['portfolio']=df_manual['portval']/df_manual['portval'][0]
    
    print(df_manual['portfolio'][-1])
    
    # plot portfolio chart in-sample
    plt.figure(n,figsize=(12,7))
    if n==1:
        title='Portfolio Comparison in-sample'
    else:
        title='Portfolio Comparison out-of-sample'
    plt.title(title)
    plt.plot(df_benm.index, df_benm['portfolio'], label='Benchmark',color='green')
    plt.plot(df_manual.index, df_manual['portfolio'],color='red', label='Manual Strategy')
    plt.xlabel('Time')
    plt.ylabel('portfolio')
    long_entries=df_orders[df_orders[symbol]>0]
    short_entries=df_orders[df_orders[symbol]<0]
    #print(long_entries)
    ymin1=[]
    for idx,row in long_entries.iterrows():
        ymin1.append(df_manual.loc[idx, 'portfolio'])
    ymax1=[x+0.1 for x in ymin1]
    
    ymin2=[df_manual.loc[idx, 'portfolio'] for idx,i in short_entries.iterrows()]
    ymax2=[x+0.1 for x in ymin2]
    
    #ax=plt.gca()
    #ymin,ymax=ax.get_ylim()
    plt.vlines(long_entries.index, ymin1,ymax1,colors='blue',label='BUY')
    plt.vlines(short_entries.index, ymin2, ymax2, colors='black', label='SELL')
    plt.legend(loc=2)
    #plt.show()
    plt.savefig(title)
    
    # table summarizes statistics
    cum_bench=df_benm['portfolio'][-1]-df_benm['portfolio'][0]
    cum_manual=df_manual['portfolio'][-1]-df_manual['portfolio'][0]
    print('------------------------------------------------')
    print('the cum_ret of the benchmark is {}.'.format(cum_bench))
    print('the cum_ret of the manual is {}.'.format(cum_manual))
    
    #stdev daily return
    daily_return_manual=df_manual['portval'][1:]/df_manual['portval'].shift(1)-1
    daily_return_bench=df_benm['portval'][1:]/df_benm['portval'].shift(1)-1
    std_dai_ret_manual=daily_return_manual.std()
    std_dai_ret_bench=daily_return_bench.std()
    print('------------------------------------------------')
    print('the stdev daily_ret of the benchmark is {}.'.format(std_dai_ret_bench))
    print('the stdev daily_ret of the manual is {}.'.format(std_dai_ret_manual))
    
    #avg daily return
    avg_dai_ret_manual=daily_return_manual.mean()
    avg_dai_ret_bench=daily_return_bench.mean()
    print('------------------------------------------------')
    print('the avg_daily_ret of the benchmark is {}.'.format(avg_dai_ret_bench))
    print('the avg_daily_ret of the manual is {}.'.format(avg_dai_ret_manual))
    
    #Sharpe Ratio
    sharpe_manual=(252**0.5)*daily_return_manual.mean()/daily_return_manual.std()
    sharpe_bench=(252**0.5)*daily_return_bench.mean()/daily_return_bench.std()
    print('------------------------------------------------')
    print('the sharpe ratio of the benchmark is {}.'.format(sharpe_bench))
    print('the sharpe ratio of the manual is {}.'.format(sharpe_manual))
    
    
def author():
    return 'whuang98'

if __name__=="__main__":
    plot_data()
    plot_data(sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31),n=2)
    #testPolicy()
