import praw
from pmaw import PushshiftAPI
import pandas as pd
import datetime as dt

from app.models import Submission, Comment, Topic
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

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + dt.timedelta(n)

    def api_f(self, date):
        gen = self.api.search_submissions(
                                    user = 'AutoModerator',
                                    title='Daily Discussion - '+str(date),
                                    selftext="Welcome to the Daily Discussion.",
                                    subreddit = 'cryptocurrency',
                                    limit = 200,
        #                              num_comments = '>50',
                                    sort='desc',
        #                              q='*'
            )
        df = pd.DataFrame(gen)
        return df
    
    def get_df(self, start_date, end_date):
        x=pd.DataFrame()
        for single_date in self.daterange(start_date, end_date):
            date = single_date.strftime("%B %d, %Y")
            print(self.api_f(date))
            x = x.append(self.api_f(date))
        return x[['id','num_comments','created_utc']]
    
    def get_comments(self):
        gen_topic = Topic.objects.filter(type='gen')[0]
        btc_topic = Topic.objects.filter(type='btc')[0]
        eth_topic = Topic.objects.filter(type='eth')[0]
        start_date = dt.date(2018, 4, 22)
        end_date = dt.date(2021, 5, 11)
        df = self.get_df(start_date, end_date)

        data = []
        for i in df.iterrows():
            submission = self.reddit.submission(i[1].id)
            submission.comment_sort = "top"
            comment_dict_list = []
            for j, top_level_comment in enumerate(submission.comments[0:30]):
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
                    'date': dt.datetime.utcfromtimestamp(top_level_comment.created_utc).strftime('%Y-%m-%d'),
                    'topic': topics
                    }
                comment_dict_list.append(comment_dict)
            data.append({
                'id': i[1].id,
                'post_date': dt.datetime.utcfromtimestamp(i[1].created_utc).strftime('%Y-%m-%d'),
                'comments': comment_dict_list
            })
        return data

    def append_data(self):
        for i in self.get_comments():
            submission = Submission(date=i['post_date'], id=i['id'])
            submission.save()
            # self.stdout.write(self.style.SUCCESS('Submission saved'))
            for j in i['comments']:
                comment = Comment(id=j['id'],text=j['text'], score=j['score'], date=j['date'], submission=submission)
                comment.save()
                if len(j['topic']) > 1:
                    print('multitopic')
                comment.topic.add(*j['topic'])

    def handle(self, *args, **options):
        try:
            self.append_data()
        except:
            raise CommandError('An error has occurred.')
