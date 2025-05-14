import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

MODEL_PATH = 'ai_model.pkl'

def train_model(stock='AAPL'):
    df = yf.download(stock, period='1y', interval='1d')
    df['Return'] = df['Close'].pct_change()
    df['Target'] = (df['Return'].shift(-1) > 0).astype(int)
    df.dropna(inplace=True)

    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    X = df[features]
    y = df['Target']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump((model, scaler), MODEL_PATH)
    return model, scaler

def predict_direction(stock='AAPL'):
    if not os.path.exists(MODEL_PATH):
        train_model(stock)
    
    model, scaler = joblib.load(MODEL_PATH)
    df = yf.download(stock, period='5d', interval='1d')
    X_new = df[['Open', 'High', 'Low', 'Close', 'Volume']].tail(1)
    X_scaled = scaler.transform(X_new)
    prediction = model.predict(X_scaled)
    return 'UP' if prediction[0] == 1 else 'DOWN'
