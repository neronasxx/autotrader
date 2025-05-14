import talib
import pandas as pd

def apply_indicators(df):
    close = df['Close']
    df['RSI'] = talib.RSI(close, timeperiod=14)
    df['MACD'], df['MACD_signal'], _ = talib.MACD(close)
    df['EMA50'] = talib.EMA(close, timeperiod=50)
    df['EMA200'] = talib.EMA(close, timeperiod=200)
    df['UpperBand'], df['MiddleBand'], df['LowerBand'] = talib.BBANDS(close)
    return df
