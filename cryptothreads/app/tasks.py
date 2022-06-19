from celery import shared_task
import praw
from pmaw import PushshiftAPI
import pandas as pd
from datetime import datetime
import datetime as dt
from app.models import Submission, Comment, Topic, TradingDay
from django.core.management.base import BaseCommand, CommandError
import requests

class Update():
    def __init__(self):
        self.api = PushshiftAPI()
        self.reddit = praw.Reddit(
        client_id="3B_hPuLSNInJTsozWMHqcA",
        client_secret="mMcsjS3apcp-wIxm2mcGNlEaAZsn_A",
        user_agent="web:crypto-comment-sentiment:v1.0.0 (by /u/kash_sam_)",
        )
        today = dt.datetime.now()
        d = dt.timedelta(days = 1)
        a = today - d
        self.yesterday = a

    def update_eth(self):
        start_epoch = int(self.a.timestamp())
        x = self.api.search_submissions(
                        title = 'Daily Discussion',
                        stickied= 'true',
                        subreddit = 'ethtrader',
                        sort = 'desc',
                        limit = 1
                            )  
        eth = pd.DataFrame(x)
        eth[["created_utc"]] = eth[["created_utc"]].apply(pd.to_datetime, unit='s')
        eth['created_utc'] = eth['created_utc'].dt.date
        submission = Submission(id=eth.id[0], date=eth.created_utc[0], subreddit='ethtrader')
        submission.save()
        return eth 
    
    def update(self, subreddit):
        if subreddit=='ethtrader': return self.update_eth
        x = self.api.search_submissions(
                        title = 'Daily Discussion',
                        stickied= 'true',
                        subreddit = subreddit,
                        sort = 'desc',
                        after = self.yesterday
                            )  
    def process_df(self):
        df = pd.DataFrame(self.update())
        # df[["created_utc"]] = df[["created_utc"]].apply(pd.to_datetime, unit='s')
        # df['created_utc'] = df['created_utc'].dt.date
        crypto_threads = df[['id','num_comments','created_utc']]
        print(crypto_threads)
        for i in crypto_threads.iterrows():
            comment = Submission.objects.filter(id=i[1].id)
            if comment:
                comment.delete()
                comment.save()

        print(crypto_threads)
        return crypto_threads

    # to get top 10 for each day on multi-day post: sort by popularity, 
    def get_comments(self):
        gen_topic = Topic.objects.filter(type='gen')[0]
        btc_topic = Topic.objects.filter(type='btc')[0]
        eth_topic = Topic.objects.filter(type='eth')[0]
        df = self.process_df()
        data = []
        for i in df.iterrows():
            submission = self.reddit.submission(i[1].id)
            submission.comment_sort = "top"
            comment_dict_list = []
            for j, top_level_comment in enumerate(submission.comments[0:50]):
                topics = []
                special_topic = False
                if j <= 10:
                    topics.append(gen_topic)
                body_lower = top_level_comment.body.lower()
                if ' eth ' in body_lower or 'ethereum' in body_lower:
                    topics.append(eth_topic)
                    special_topic = True
                if ' btc ' in body_lower or 'bitcoin' in body_lower:
                    topics.append(btc_topic)
                    special_topic = True
                if not special_topic and j > 10:
                    continue
                comment_dict = {
                    'id': top_level_comment.id,
                    'text': top_level_comment.body,
                    'score': top_level_comment.score, 
                    'date': datetime.utcfromtimestamp(top_level_comment.created_utc).strftime('%Y-%m-%d'),
                    'topic': topics
                    }
                comment_dict_list.append(comment_dict)
            data.append({
                'id': i[1].id,
                'post_date': datetime.utcfromtimestamp(i[1].created_utc).strftime('%Y-%m-%d'),
                'comments': comment_dict_list
            })
        return data

    def append_data(self):
        for i in self.get_comments():
            if not Submission.objects.filter(date=i['post_date']):
            # submission = Submission.objects.filter(date=i['post_date'])
                submission = Submission(id=i['id'], date=i['post_date'], subreddit='bitcoin')
                submission.save()
                # self.stdout.write(self.style.SUCCESS('Submission saved'))
                for j in i['comments']:
                    # print(j)
                    # print(submission)
                    # if not Comment.objects.filter(id=j['id']):
                        print(2)
                        comment = Comment(id=j['id'],text=j['text'], score=j['score'], date=j['date'], submission=submission)
                        comment.save()
                        print(3)
                        if len(j['topic']) > 1:
                            print('multitopic')
                        comment.topic.add(*j['topic'])
                        # self.stdout.write(self.style.SUCCESS('Comment saved'))
    ### UPDATE PRICE ###
    def get_price_data(self, days):
        print("2")

        btc_data = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days={0}'.format(days)).json()['prices']
        btc_price = pd.DataFrame(data=btc_data, columns=['time','btc_price'])
        btc_price["time"]= btc_price["time"].apply(pd.to_datetime, unit='ms').apply(lambda x: str(x)[:10])
        print('2.1')
        eth_data = requests.get('https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days={0}'.format(days)).json()['prices']
        eth_price = pd.DataFrame(data=eth_data, columns=['time','eth_price'])
        eth_price["time"]= eth_price["time"].apply(pd.to_datetime, unit='ms').apply(lambda x: str(x)[:10])
        
        return (btc_price, eth_price)
    
    def aggregate_data(self):
        total_data = self.get_total_cap_data()
        data_tuple = self.get_price_data()
        print("3")
        btc_price, eth_price = data_tuple[0], data_tuple[1]
        print("3.1")
        total_df = total_data.merge(btc_price, how='inner', on='time').sort_values(by='time', axis=0)
        print("3.2")
        total_df = total_df.merge(eth_price, how='inner', on='time').sort_values(by='time', axis=0)
        total_df['time'] = total_df['time'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d'))
        return total_df
    
    # def get_comments(self, date):

    def add_data(self):
        total_df = self.aggregate_data()
        print("4")
        for i in total_df.iterrows():
            trading_day = TradingDay(date=i[1]['time'],
                                    crypto_cap=i[1]['open'],
                                    bitcoin_price=i[1]['btc_price'],
                                    ethereum_price=i[1]['eth_price'])
                                    # comments=Comment.objects.filter(date=i[1]['time']))
            trading_day.save()

@shared_task(name='update_db')
def stuff():
    update = Update()
    update.add_data()