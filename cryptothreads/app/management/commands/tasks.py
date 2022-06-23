from celery import shared_task
import praw
from pmaw import PushshiftAPI
import pandas as pd
from datetime import datetime
import datetime as dt
from app.models import Submission, Comment, Topic, TradingDay
from django.core.management.base import BaseCommand, CommandError
import requests

class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.api = PushshiftAPI()
        self.reddit = praw.Reddit(
        client_id="3B_hPuLSNInJTsozWMHqcA",
        client_secret="mMcsjS3apcp-wIxm2mcGNlEaAZsn_A",
        user_agent="web:crypto-comment-sentiment:v1.0.0 (by /u/kash_sam_)",
        )
        today = dt.datetime.now()
        d = dt.timedelta(days = 2)
        a = today - d
        self.yesterday = int(a.timestamp())
        self.gen_topic = Topic.objects.filter(type='gen')[0]
        self.btc_topic = Topic.objects.filter(type='btc')[0]
        self.eth_topic = Topic.objects.filter(type='eth')[0]

    def update(self, subreddit):
        x = self.api.search_submissions(
                        title = 'Daily Discussion',
                        stickied= 'true',
                        subreddit = subreddit,
                        sort = 'desc',
                        after = self.yesterday,
                        limit = 2
                            )  
        eth = pd.DataFrame(x)
        print(eth)
        if not eth.empty and not Submission.objects.filter(id=eth.id[0]):            
            eth[["created_utc"]] = eth[["created_utc"]].apply(pd.to_datetime, unit='s')
            eth['created_utc'] = eth['created_utc'].dt.date
            submission = Submission(id=eth.id[0], date=eth.created_utc[0], subreddit=subreddit)
            submission.save()
            print(submission)
            api = self.reddit.submission(i[1].id)
            api.comment_sort = "top"
            for i in api.comments[0:100]:
                print(i)
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
                    print(c)
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

        except:
            raise CommandError('An error has occurred.')