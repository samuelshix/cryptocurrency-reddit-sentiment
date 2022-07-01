import praw
from pmaw import PushshiftAPI
import pandas as pd
from datetime import datetime
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
        today = dt.datetime.now()
        d = dt.timedelta(days = 4)
        a = today - d
        self.ten_days = int(a.timestamp())

    def get_discussion_submissions(self, subreddit):
        print('Using {0} subreddit...'.format(subreddit))
        url = f'https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&title=discussion&stickied=true&after=5d'
        return requests.get(url).json()

    def process_df(self, subreddit):
        data = self.get_discussion_submissions(subreddit)['data']
        if not data:
            pass
        return data

    # to get top 15 comments for each day: sort by popularity, 
    def get_comments(self, subreddit):
        gen_topic = Topic.objects.filter(type='gen')[0]
        btc_topic = Topic.objects.filter(type='btc')[0]
        eth_topic = Topic.objects.filter(type='eth')[0]
        data1 = self.process_df(subreddit)
        data = []
        for i in data1:
            # print(i['id'])
            submission = self.reddit.submission(i['id'])
            print(submission)
            submission.comment_sort = "top"
            comment_dict_list = []
            # if i[1]['num_comments'] > 2000:
            # submission.comments.replace_more(limit=0)
            #     end_index = len(submission.comments)
            # else:
            #     end_index = 10
            for j, top_level_comment in enumerate(submission.comments[0:10]):
                if top_level_comment.score > 5:
                    topics = []
                    topics.append(gen_topic)
                    # topics.append(eth_topic)
                    # special_topic = False
                    # if j <= 10:
                    #     topics.append(gen_topic)
                    body_lower = top_level_comment.body.lower()
                    if ' eth ' in body_lower or 'ethereum' in body_lower or subreddit=='ethfinance' or subreddit=='ethtrader' or subreddit=='ethereum':
                        topics.append(eth_topic)
                        # special_topic = True
                    if ' btc ' in body_lower or 'bitcoin' in body_lower or subreddit=='bitcoin':
                        topics.append(btc_topic)
                    #     special_topic = True
                    # if not special_topic and j > 10:
                    #     continue
                    comment_dict = {
                        'id': top_level_comment.id,
                        'text': top_level_comment.body,
                        'score': top_level_comment.score, 
                        'date': datetime.utcfromtimestamp(top_level_comment.created_utc).strftime('%Y-%m-%d'),
                        'topic': topics
                        }
                    # print(comment_dict)
            data.append({
                'id': i['id'],
                'post_date': datetime.utcfromtimestamp(i['created_utc']).strftime('%Y-%m-%d'),
                'comments': comment_dict_list
            })
        print('Appending Data')
        return data

    def append_data(self, subreddit):
        for i in self.get_comments(subreddit):
            if not Submission.objects.filter(id=i['id']):
                submission = Submission(date=i['post_date'], id=i['id'], subreddit=subreddit)
                submission.save()
            # submission = Submission.objects.get(id=i['id'])
            for j in i['comments']:
                if not Comment.objects.filter(id=j['id']):
                    comment = Comment(id=j['id'],text=j['text'], score=j['score'], date=j['date'], submission=submission)
                    comment.save()
                    comment.topic.add(*j['topic'])
        
    def handle(self, *args, **options):
        try:
            subreddits = ['bitcoin','cryptocurrency', 'ethereum', 'ethtrader', 'ethfinance']
            for i in subreddits: self.append_data(i)
                # self.append_data('ethfinance')
            # self.append_comments()
            # self.append_data('cryptocurrency')
            # self.append_data('cryptocurrency')
            print('Success!')
        except:
            raise CommandError('An error has occurred.')

# def main():
#     append_data()
#     print('Job done!')
# if __name__ == '__main__':
#     main()
