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
            'subreddit',
            nargs=1,
            type=str
        )
    # def get_discussion_submissions(self):
        # return self.api.search_submissions(user = 'AutoModerator',
        #                             title = 'Daily Discussion',
        #                             subreddit = 'cryptocurrency',
        #                             sort = 'desc',
        #                             num_comments = '>50',
        #                             limit = 2000)

    def get_discussion_submissions(self, subreddit):
        today = dt.datetime.now()
        d = dt.timedelta(days = 126)
        a = today - d
        start_epoch = int(a.timestamp())
        print('Using {0} subreddit...'.format(subreddit))
        if subreddit == 'cryptocurrency':
            return self.api.search_submissions(user = 'AutoModerator',
                            title = 'Daily Discussion',
                            subreddit = 'cryptocurrency',
                            sort = 'desc',
                            num_comments = '>50',
                            )
        elif subreddit == 'ethtrader':
            return self.api.search_submissions(
                                        title = 'Daily Discussion',
                                        subreddit = 'ethtrader',
                                        sort = 'desc',
                                        # num_comments = '>100',
                                        )
        elif subreddit == 'bitcoin':
            return self.api.search_submissions(
                                        title = 'Daily Discussion, ',
                                        subreddit = 'bitcoin',
                                        sort = 'desc',
                                        # num_comments = '>100',
                                        after= start_epoch
                                        )
    def process_df(self, subreddit):
        df = pd.DataFrame(self.get_discussion_submissions(subreddit))
        # df[["created_utc"]] = df[["created_utc"]].apply(pd.to_datetime, unit='s')
        # df['created_utc'] = df['created_utc'].dt.date
        crypto_threads = df[['id','num_comments','created_utc']]
        print('Using df:')
        print(crypto_threads)
        return crypto_threads

    # to get top 10 for each day on multi-day post: sort by popularity, 
    def get_comments(self, subreddit):
        gen_topic = Topic.objects.filter(type='gen')[0]
        btc_topic = Topic.objects.filter(type='btc')[0]
        eth_topic = Topic.objects.filter(type='eth')[0]
        df = self.process_df(subreddit)
        data = []
        for i in df.iterrows():
            # print(i[1])
            submission = self.reddit.submission(i[1].id)
            submission.comment_sort = "top"
            comment_dict_list = []
            if i[1]['num_comments'] > 2000:
                submission.comments.replace_more(limit=0)
                end_index = len(submission.comments)
            else:
                end_index = 15
            for j, top_level_comment in enumerate(submission.comments[0:end_index]):
                topics = []
                topics.append(gen_topic)

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
                # print(comment_dict)
                comment_dict_list.append(comment_dict)
            data.append({
                'id': i[1].id,
                'post_date': datetime.utcfromtimestamp(i[1].created_utc).strftime('%Y-%m-%d'),
                'comments': comment_dict_list
            })
            # print(data)
        print('data dict:')
        return data

    def append_data(self, subreddit):
        for i in self.get_comments(subreddit):
            print(i)
            submission = Submission(date=i['post_date'], id=i['id'], subreddit=subreddit)
            submission.save()
            # self.stdout.write(self.style.SUCCESS('Submission saved'))
            for j in i['comments']:
                comment = Comment(id=j['id'],text=j['text'], score=j['score'], date=j['date'], submission=submission)
                comment.save()
                comment.topic.add(*j['topic'])
                # self.stdout.write(self.style.SUCCESS('Comment saved'))

    def handle(self, *args, **options):
        try:
            # self.append_data(options['subreddit'][0])
            self.append_data('bitcoin')
            self.append_data('cryptocurrency')
            self.append_data('ethtrader')
            print('Success!')
            # self.stdout.write(self.style.SUCCESS('Success!'))
        except:
            raise CommandError('An error has occurred.')

# def main():
#     append_data()
#     print('Job done!')
# if __name__ == '__main__':
#     main()
