import requests
from textblob import TextBlob

def get_news_sentiment(stock):
    url = f"https://newsapi.org/v2/everything?q={stock}&apiKey=your_newsapi_key"
    response = requests.get(url).json()
    articles = response.get("articles", [])[:5]
    sentiment_score = 0
    for article in articles:
        sentiment_score += TextBlob(article['title']).sentiment.polarity
    return sentiment_score / max(len(articles), 1)
