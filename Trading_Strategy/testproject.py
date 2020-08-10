import ManualStrategy as ms
import StrategyLearner as sl
import experiment1 as ex1
import experiment2 as ex2
import datetime as dt


def calls():
    ms.plot_data()
    ms.plot_data(sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31),n=2)
    ex1.compare()
    ex2.impact_effect()
    

def author():
    return 'whuang98'

if __name__=="__main__":
    calls()
