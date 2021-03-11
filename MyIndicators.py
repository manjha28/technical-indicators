import pandas as pd
import numpy as np
import OtherIndicator
from nsepy import get_history
from datetime import date


def SMA(df, calcby, period, colname):
    df[colname] = df[calcby].rolling(window=period).mean()
    df[colname].fillna(0, inplace=True)
    return df


def EMA(df, calcby, period, colname):
    con = pd.concat([df[:period][calcby].rolling(window=period).mean(), df[period:][calcby]])
    df[colname] = con.ewm(span=period, adjust=False).mean()
    df[colname].fillna(0, inplace=True)
    return df

def RSI(df,calcby="Close",period = int):
    """RSI = 100 – 100 / ( 1 + RS )"""

    delta = df[calcby].diff()
    up, down = delta.copy(), delta.copy()

    """ For each bar, up move (U) equals:
Closet – Closet-1 if the price change is positive
Zero if the price change is negative or zero

Down move (D) equals:
The absolute value of Closet – Closet-1 if the price change is negative
Zero if the price change is positive or zero"""

    up[up < 0] = 0
    down[down > 0] = 0

    AvgUp = up.ewm(com=period - 1, adjust=False).mean()
    AvgDown = down.ewm(com=period - 1, adjust=False).mean().abs()
    """RS = Relative Strength = AvgUp / AvgDown
    AvgU = average of all up moves in the last N price bars
    AvgD = average of all down moves in the last N price bars
    N = the period of RSI"""

    df['RSI_' + str(period)] = 100 - 100 / (1 + AvgUp / AvgDown)
    df['RSI_' + str(period)].fillna(0, inplace=True)

    return df

def PivotPoints(df,period = 1,High = "High",Low="Low",Close = "Close"):
    pp = (df[:period][High]+df[:period][Low]+df[:period][Close])/3
    df['PP'] = pp

    return df



def MASCAN(watchlist):
    for name in watchlist:
        df = get_history(symbol= name , start=date(2021,2,10), end=date(2021,2,15))
        # print(RSI(df,"Close",9))
        # print(OtherIndicator.EMA(df,"Open","n9ema",9))
        # print(RSI(df,period=14))
        print(PivotPoints(df))


if __name__ == '__main__':
    MASCAN(["SBIN","ITC"])