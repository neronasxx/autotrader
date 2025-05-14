import streamlit as st
import yfinance as yf
from bot import trade
from ai_model import predict_direction

st.set_page_config(page_title="Auto Trader Dashboard", layout="wide")
st.title("📈 Auto Trading Bot Dashboard")

stock = st.selectbox("Choose a stock to analyze", ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN", "META", "GOOG", "NFLX", "AMD"])
if st.button("Run Trade Strategy Now"):
    trade(stock)
    st.success("Strategy executed.")

st.subheader("📊 Live Stock Data")
data = yf.download(stock, period="5d", interval="1h")
st.line_chart(data['Close'])

st.subheader("🤖 AI Model Prediction")
prediction = predict_direction(stock)
st.metric(label="AI Forecast for Tomorrow", value=prediction)
