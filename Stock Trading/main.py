import os

import requests
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime as dt
from datetime import timedelta as td

NEWS_KEY = os.getenv('NEWS_API')
STOCK_KEY = os.getenv('STOCK_API')

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey":STOCK_KEY
}

news_params = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_KEY,
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
stock = response.json()["Time Series (Daily)"]

media = requests.get(url=NEWS_ENDPOINT, params=news_params)
news = media.json()['articles'][:4]

yesterday = dt.today().now().date() - td(days=1)
b4_yesterday = dt.today().now().date() - td(days=2)

yesterday_price = float([value for (key, value) in stock.items() if str(yesterday) in key][0]['4. close'])
b4_yesterday_price = float([value for (key, value) in stock.items() if str(b4_yesterday) in key][0]['4. close'])

diff = abs(yesterday_price - b4_yesterday_price)
percent_diff = round((diff/yesterday_price) * 100, 1)

up_down = None

if diff > 0:
    up_down = "⬆️"
else:
    up_down = '⬇️'

if percent_diff > 3:
    articles = [f"{STOCK_NAME}: {up_down}{percent_diff}\nHeadline: {article['title']}\n \nBrief:{article['description']}" for
                article in news]
    print(articles)
