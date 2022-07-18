from celery import shared_task
import praw
from pmaw import PushshiftAPI
import pandas as pd
from datetime import datetime
import datetime as dt
from app.models import Submission, Comment, Topic, TradingDay
from django.core.management.base import BaseCommand, CommandError
import requests
import os
class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.api = PushshiftAPI()
        self.reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent=os.getenv("USER_AGENT"),
        )
        today = dt.datetime.now()
        d = dt.timedelta(days = 2)
        a = today - d
        self.yesterday = int(a.timestamp())
        self.gen_topic = Topic.objects.filter(type='gen')[0]
        self.btc_topic = Topic.objects.filter(type='btc')[0]
        self.eth_topic = Topic.objects.filter(type='eth')[0]

    def update(self, subreddit):
        url = f'https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&title=discussion&stickied=true&after=2d'
        requests.get(url)
        eth = requests.get(url).json()['data']
        if eth: 
            if Submission.objects.filter(id=eth[0]['id]']):            
                submission = Submission(id=eth[0]['id'], date=datetime.fromtimestamp(eth[0]['created_utc'].strftime('%Y-%m-%d'), subreddit=subreddit))
                submission.save()
                api = self.reddit.submission(submission.id)
                api.comment_sort = "top"
                for i in api.comments[0:10]:
                    if not Comment.objects.filter(id=i.id):
                        topics = [self.gen_topic]
                        body_lower = i.body.lower()
                        if ' eth ' in body_lower or 'ethereum' in body_lower:
                            topics.append(self.eth_topic)
                        elif ' btc ' in body_lower or 'bitcoin' in body_lower:
                            topics.append(self.btc_topic)
                        c = Comment(id=i.id,text=i.body, score=i.score, 
                        date=datetime.utcfromtimestamp(i.created_utc).strftime('%Y-%m-%d'),
                        submission=submission)
                        c.save()
                        c.topic.add(*topics)
        return eth

    def update_eth(self):
        self.update('ethtrader')

    def update_btc(self):
        self.update('bitcoin')

    def update_cry(self):
        self.update('cryptocurrency')

# GET PRICE
    def get_price_data(self):
        print("2")

        btc_data = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1').json()['prices']
        btc_price = pd.DataFrame(data=btc_data, columns=['time','btc_price'])
        btc_price["time"]= btc_price["time"].apply(pd.to_datetime, unit='ms').apply(lambda x: str(x)[:10])

        print(btc_price.iloc[-1].time)
        print(btc_price.iloc[-1].btc_price)
        eth_data = requests.get('https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=1').json()['prices']
        eth_price = pd.DataFrame(data=eth_data, columns=['time','eth_price'])
        eth_price["time"]= eth_price["time"].apply(pd.to_datetime, unit='ms').apply(lambda x: str(x)[:10])
        print(eth_price.iloc[-1].time)
        print(eth_price.iloc[-1].eth_price)   
        session = requests.Session()
        url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'cca25091-2a4a-43f3-855b-e760a8aa859f',
        }
        session.headers.update(headers)
        response = session.get(url)
        crypto_cap = response.json()['data']['quote']['USD']['total_market_cap']

        t = TradingDay(date=btc_price.iloc[-1].time,
                    crypto_cap=crypto_cap,
                    bitcoin_price=btc_price.iloc[-1].btc_price,
                    ethereum_price=eth_price.iloc[-1].eth_price)
        if not TradingDay.objects.filter(date = btc_price.iloc[-1].time):
            t.save()
        return t
    # def get_comments(self, date):

    def add_data(self):
        total_df = self.aggregate_data()
        print("4")
        for i in total_df.iterrows():
            trading_day = TradingDay(date=i[1]['time'],
                                    crypto_cap=i[1]['open'],
                                    bitcoin_price=i[1]['btc_price'],
                                    ethereum_price=i[1]['eth_price'])
            trading_day.save()
    def handle(self, *args, **options):
        try:
            self.get_price_data()
            subreddits = ['bitcoin','cryptocurrency', 'ethereum', 'ethtrader', 'ethfinance']
            for i in subreddits: self.update(i)
        except:
            raise CommandError('An error has occurred.')