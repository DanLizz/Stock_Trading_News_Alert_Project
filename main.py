import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

account_sid = "xxxxxxxxx"
auth_token = "xxxxxxxxx"

# STEP 1:When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

AV_Endpoint = "https://www.alphavantage.co/query"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": "XXXXXXXXXXXXXXXXX",
}

NEWS_Endpoint = "https://newsapi.org/v2/everything"

response = requests.get(AV_Endpoint, params=stock_params)
stock_data = response.json()
stock_slice = stock_data["Time Series (Daily)"]
day = 0
stock_open_data = []
stock_close_data = []

for daily_data in stock_slice:
    news_params = {
        "q": "tesla",
        "from": "yesterday",
        "sortBy": "publishedAt",
        "apiKey": "794ac5b2403b4e6db5a3e7770de81fe4",
    }

    news_response = requests.get(NEWS_Endpoint, params=news_params)

    if day < 2:
        stock_open = stock_slice[daily_data]["1. open"]
        stock_open_data.append(stock_open)
        stock_close = stock_slice[daily_data]["4. close"]
        stock_close_data.append(stock_close)

        print(f"Open: {stock_open}")
        print(f"Close: {stock_close}")

        TSLA_up = float(stock_open_data[day]) > float(stock_close_data[day-1])*0.05
        TSLA_down = float(stock_open_data[day]) < float(stock_close_data[day-1])*0.05

        if  TSLA_down or TSLA_up:
            print("Get News")
            news_data = news_response.json()
            print(news_data["articles"])
            proxy_client = TwilioHttpClient()
            proxy_client.session.proxies = {'https': os.environ["https_proxy"]}
            client = Client(account_sid, auth_token, http_client=proxy_client)

            TSLA_up_message = f"""
                TSLA: 🔺5%
                Headline: {news_data["articles"][0]["title"]}
                Brief: {news_data["articles"][0]["description"]}"""

            TSLA_down_message = f"""
                            TSLA: 🔻5%
                            Headline: {news_data["articles"][0]["title"]}
                            Brief: {news_data["articles"][0]["description"]}"""
            if TSLA_up:
                print(TSLA_up_message)
                message = client.messages \
                    .create(body=TSLA_up_message, from_='+1xxxxxxxxx', to='+1xxxxxxxxx')
            elif TSLA_down:
                print(TSLA_down_message)
                message = client.messages \
                    .create(body=TSLA_down_message, from_='+1xxxxxxxxx', to='+1xxxxxxxxx')

            day += 1

