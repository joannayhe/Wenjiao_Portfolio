
import pandas as pd
import datetime as dt
from util import get_data, plot_data
import matplotlib.pyplot as plt



def get_df(symbol='JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31)):
    df_price=get_data([symbol], pd.date_range(sd, ed))
    df_price.fillna(method='ffill', inplace=True)
    df_price.fillna(method='bfill', inplace=True)
    if symbol!='SPY':
        df_price.drop(['SPY'], axis=1,inplace=True)
    normed_price=df_price/df_price.iloc[0,:]
    return normed_price


def price_SMA(normed_price, win=20):
    symbol=normed_price.columns[0]
    sma=normed_price.copy()
    sma['SMA']=normed_price.rolling(window=win).mean()
    #sma.fillna(method='bfill',inplace=True)
    sma['price/sma']=sma[symbol]/sma['SMA']
    p_sma=sma['price/sma'].to_frame()
   
    return p_sma


def bollinger_bands(normed_price, win=20):
    symbol=normed_price.columns[0]
    df_bb=normed_price.copy()
    df_bb['std']=normed_price.rolling(window=win).std()
    df_bb['sma']=normed_price.rolling(window=win).mean()
    #df_bb.fillna(method='bfill',inplace=True)
    df_bb['Upper']=df_bb['sma']+(2*df_bb['std'])
    df_bb['Lower']=df_bb['sma']-(2*df_bb['std'])
    df_bb['bb']=(df_bb[symbol]-df_bb['sma'])/(2*df_bb['std'])
    df_bb=df_bb['bb'].to_frame()
    
    return df_bb
    
    
def EMA(normed_price, win=20):
    symbol=normed_price.columns[0]
    EMA=normed_price.copy()
    EMA[symbol+'sma']=normed_price.rolling(window=win).mean()
    #EMA.fillna(method='bfill',inplace=True)
    EMA[symbol+'ema']=normed_price[symbol].ewm(span=win, adjust=False).mean()
    EMA=EMA[symbol+'ema'].to_frame()
    #print(EMA)
    return EMA


def momentum(normed_price, win=20):
    symbol=normed_price.columns[0]
    df_momen=normed_price.copy()
    df_momen[symbol+'momen']=df_momen[symbol]/df_momen[symbol].shift(periods=win)-1
    df_momen.fillna(method='bfill',inplace=True)
    #print(df_momen)
    return df_momen


def Force_index(normed_price, win=13):
    symbol=normed_price.columns[0]
    start_date=normed_price.index[0]
    end_date=normed_price.index[-1]
    df_volume=get_data([symbol], pd.date_range(start_date, end_date), colname='Volume')
    df_volume.drop(['SPY'], axis=1, inplace=True)
    df_force_index=normed_price.copy()
    df_force_index['volume']=df_volume
    df_force_index['force index']=df_force_index[symbol].diff(periods=1)*df_force_index['volume']
    #df_force_index.fillna(method='bfill',inplace=True)
    df_force_index['roll-force-index']=df_force_index['force index'].ewm(span=win, adjust=False).mean()
    df_force_index=df_force_index['roll-force-index'].to_frame()
    #print(df_force_index)
    return df_force_index

def author():
    return 'whuang98'


def main(symbol='JPM'):
    #generate the charts that illustrate indicators
    
    
    #1. Price/SMA
    df=get_df()
    df_sma=price_SMA(normed_price=df)
    
    plt.figure(1, figsize=(8,5))
    plt.title('Indicator Price/SMA')
    plt.plot(df_sma.index, df_sma[symbol], label='adj close price')
    plt.plot(df_sma.index, df_sma['SMA'])
    plt.plot(df_sma.index, df_sma['price/sma'])
    plt.axhline(y=1, color='grey', linestyle='dashed')
    plt.axhline(y=1.05, color='grey', linestyle='dashed')
    plt.axhline(y=0.95, color='grey', linestyle='dashed')
    plt.xlabel('Time')
    plt.ylabel('normalized price\nPrice/SMA value')
    #plt.xticks(df_sma.index[::30])
    plt.legend()
    plt.savefig('price_sma')
    #plt.show()
    
    #2. bollinger bands
    df_bb=bollinger_bands(normed_price=df)
    
    plt.figure(2, figsize=(9,6))
    plt.subplot(2,1,1)
    plt.title('Indicator bollinger bands')
    plt.plot(df_bb.index, df_bb[symbol], label='adj close price')
    plt.plot(df_bb.index, df_bb['sma'])
    plt.plot(df_bb.index, df_bb['Upper'])
    plt.plot(df_bb.index, df_bb['Lower'])
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('normalized price')
    
    plt.subplot(2,1,2)
    plt.plot(df_bb.index, df_bb['bb'], label='bb value')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('BB value')
    #plt.show()
    plt.savefig('bolliger_bands')
    
    #3. EMA
    df_EMA=EMA(normed_price=df)
    df_EMA2=EMA(normed_price=df, win=50)
    
    plt.figure(3, figsize=(8,5))
    plt.title('Indicator EMA')
    plt.plot(df_EMA.index, df_EMA[symbol], label='adj close price')
    plt.plot(df_EMA.index, df_EMA[symbol+'sma'])
    plt.plot(df_EMA.index, df_EMA[symbol+'ema'], label='JMP-20-EMA')
    plt.plot(df_EMA2.index, df_EMA2[symbol+'ema'], label='JMP-50-EMA')
    plt.xlabel('Time')
    plt.ylabel('normalized price')
    plt.legend()
    #plt.show()
    plt.savefig('EMA')
    
    #4. momentum
    df_momen=momentum(normed_price=df)
    
    plt.figure(4, figsize=(8,5))
    plt.title('Indicator momentum')
    plt.subplot(2,1,1)
    plt.plot(df_momen.index, df_momen[symbol], label='adj close price')
    plt.xlabel('Time')
    plt.ylabel('normalized price')
    plt.legend()
    
    plt.subplot(2,1,2)
    plt.plot(df_momen.index, df_momen[symbol+'momen'], color='orange')
    plt.axhline(y=0, color='grey', linestyle='dashed')
    plt.xlabel('Time')
    plt.ylabel('ratio')
    plt.legend()
    plt.savefig('momentum')
    #plt.show()
    
    #5. Force Index
    df_force_index=Force_index(normed_price=df)
    
    plt.figure(5, figsize=(8,6))
    plt.subplot(2,1,1)
    plt.title('Indicator Force Index')
    
    plt.plot(df_force_index.index, df_force_index['force index'])
    plt.plot(df_force_index.index, df_force_index['13-force-index'], color='red')
    plt.axhline(y=0, color='grey', linestyle='dashed')
    plt.xlabel('Time')
    plt.ylabel('Force Index value')
    plt.legend()
    
    plt.subplot(2,1,2)
    plt.plot(df_force_index.index, df_force_index[symbol], label='adj close price', color='green')
    plt.xlabel('Time')
    plt.ylabel('normalized price')
    plt.legend()
    plt.savefig('Force Index')
    #plt.show()
    


if __name__ == '__main__':
    main()