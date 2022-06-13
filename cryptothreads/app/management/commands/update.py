import praw
from pmaw import PushshiftAPI
import pandas as pd
from datetime import datetime
import datetime as dt
from app.models import Submission, Comment, Topic
from django.core.management.base import BaseCommand, CommandError
import requests
import re
class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()

        self.api = PushshiftAPI()
        self.reddit = praw.Reddit(
        client_id="3B_hPuLSNInJTsozWMHqcA",
        client_secret="mMcsjS3apcp-wIxm2mcGNlEaAZsn_A",
        user_agent="web:crypto-comment-sentiment:v1.0.0 (by /u/kash_sam_)",
        )

    def add_arguments(self, parser):
        parser.add_argument(
            '--text',
            action='store_true',
            help='Update text'
        )

    def update_text(self):
        for comment in Comment.objects.all():
            comment.text = re.sub("'","’",comment.text)
            comment.text = re.sub("`","’",comment.text)
            comment.text = re.sub('"',"“",comment.text)
            comment.save()

    def update(self):
        today = dt.datetime.now()
        d = dt.timedelta(days = 10)
        a = today - d
        start_epoch = int(a.timestamp())
        print(start_epoch)
        return self.api.search_submissions(
                            user = 'CryptoDaily-',
                            title='Daily Discussion',
                             subreddit = 'cryptocurrency',
                            # num_comments = '>300',
                             sort='desc',
                             after= start_epoch)  

    def get_discussion_submissions(self):
        return self.api.search_submissions(user = 'AutoModerator',
                                    title = 'Daily Discussion - ',
                                    subreddit = 'cryptocurrency',
                                    # num_comments = '>300',
                                    limit = 2000,
                                    sort = 'desc')
  
    def process_df(self):
        df = pd.DataFrame(self.update())
        # df[["created_utc"]] = df[["created_utc"]].apply(pd.to_datetime, unit='s')
        # df['created_utc'] = df['created_utc'].dt.date
        crypto_threads = df[['id','num_comments','created_utc']]
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
                submission = Submission(id=i['id'], date=i['post_date'])
                submission.save()
                # self.stdout.write(self.style.SUCCESS('Submission saved'))
                for j in i['comments']:
                    # print(j)
                    # print(submission)
                    # if not Comment.objects.filter(id=j['id']):
                        print(2)
                        comment = Comment(id=j['id'],text=j['text'], score=j['score'], date=j['date'], submission=submission)
                        comment.text = re.sub("'","’",comment.text)
                        comment.text = re.sub("`","’",comment.text)
                        comment.text = re.sub('"',"“",comment.text)
                        comment.save()
                        print(3)
                        if len(j['topic']) > 1:
                            print('multitopic')
                        comment.topic.add(*j['topic'])
                        # self.stdout.write(self.style.SUCCESS('Comment saved'))

    def handle(self, *args, **options):
        try:
            if options['text']:
                self.update_text()
            else:
                self.append_data()
            # self.stdout.write(self.style.SUCCESS('Success!'))
        except:
            raise CommandError('An error has occurred.')

# def main():
#     append_data()
#     print('Job done!')
# if __name__ == '__main__':
#     main()