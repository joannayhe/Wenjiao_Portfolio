# -*- coding: utf-8 -*-
import pandas as pd  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
from util import get_data, plot_data
import datetime as dt
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
def compute_portvals(df_orders, sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),start_val = 100000, commission=9.95, impact=0.005):  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
     	  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    df_orders.sort_index(inplace=True)
    
    start_date=sd
    end_date=ed
    symbol=df_orders.columns
    
    df_adj_prices=get_data(symbol, pd.date_range(start_date, end_date))
    df_adj_prices.fillna(method='ffill', inplace=True)
    df_adj_prices.fillna(method='bfill',inplace=True)
    #print(df_adj_prices)
    df_adj_prices['Cash']=1.0
    #print(df_adj_prices)
    df_trades=df_adj_prices.copy()
    symbol=symbol[0]
    
    #fill all the columns with zero
    for col in df_trades.columns:
        df_trades[col].values[:] = 0
    #print(df_trades)
    
    for idx,row in df_orders.iterrows():
        df_trades.loc[idx,symbol]+=row[symbol]
        df_trades.loc[idx,'Cash']-=row[symbol]*df_adj_prices.loc[idx,symbol]+impact*abs(row[symbol])*df_adj_prices.loc[idx,symbol]+commission
    #print(df_trades)
    df_holdings=df_trades.copy()
    df_holdings.iloc[0,0:-1]=0
    df_holdings.iloc[0,-1]=start_val
    #print(df_holdings)
    #print(len(df_holdings))
    for i in range(len(df_holdings)):
        if i-1>=0:
            df_holdings.iloc[i,:]=df_trades.iloc[i,:]+df_holdings.iloc[i-1,:]
        else:
            df_holdings.iloc[i,:]=df_trades.iloc[i,:]+df_holdings.iloc[i,:]
    #print(df_holdings)
    
    df_values=df_holdings.copy()
    df_values=df_holdings*df_adj_prices
    #print(df_values)
    df_portval=df_values.sum(axis=1)
    df_portval=df_portval.to_frame()
    df_portval.columns=['portval']
    #print(df_portval)
    
    return df_portval
    		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    #rv = pd.DataFrame(index=portvals.index, data=portvals.values)  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    #return rv  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    #return portvals


def author():
    return 'whuang98' 		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
if __name__ == "__main__":  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    compute_portvals()

