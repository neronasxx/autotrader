from config import *
from indicators import apply_indicators
from sentiment import get_news_sentiment
import yfinance as yf
import alpaca_trade_api as tradeapi
import pandas as pd

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)

def trade(stock):
    df = yf.download(stock, period="30d", interval="1h")
    df = apply_indicators(df)
    last = df.iloc[-1]
    
    score = 0
    if last['RSI'] < 35: score += 1
    if last['MACD'] > last['MACD_signal']: score += 1
    if last['Close'] > last['EMA50']: score += 1
    if get_news_sentiment(stock) > 0.2: score += 1

    if score >= 3:
        print(f"[BUY] {stock}")
        submit_order(stock, 'buy')
    elif last['RSI'] > 70:
        print(f"[SELL] {stock}")
        submit_order(stock, 'sell')

def submit_order(symbol, side):
    price = yf.download(symbol, period="1d", interval="1m")['Close'][-1]
    buying_power = float(api.get_account().cash)
    qty = int((MAX_INVEST_PER_TRADE * buying_power) / price)
    if qty > 0:
        api.submit_order(symbol=symbol, qty=qty, side=side, type='market', time_in_force='gtc')
