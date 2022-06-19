import praw
from pmaw import PushshiftAPI
import pandas as pd
from datetime import datetime
from app.models import Submission, Comment, Topic
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()

        self.api = PushshiftAPI()
        self.reddit = praw.Reddit(
        client_id="3B_hPuLSNInJTsozWMHqcA",
        client_secret="mMcsjS3apcp-wIxm2mcGNlEaAZsn_A",
        user_agent="web:crypto-comment-sentiment:v1.0.0 (by /u/kash_sam_)",
        )

    def get_discussion_submissions(self, subreddit):
        print('Using {0} subreddit...'.format(subreddit))
        if subreddit == 'cryptocurrency':
            return self.api.search_submissions(
                            title = 'Daily Discussion',
                            stickied= 'true',
                            subreddit = 'cryptocurrency',
                            sort = 'desc',
                            )
        elif subreddit == 'ethtrader':
            return self.api.search_submissions(
                                        title = 'Daily Discussion',
                                        stickied= 'true',
                                        subreddit = 'ethtrader',
                                        sort = 'desc',
                                        )
        elif subreddit == 'bitcoin':
            return self.api.search_submissions(
                                        title = 'Daily Discussion, ',
                                        stickied= 'true',
                                        subreddit = 'bitcoin',
                                        sort = 'desc',
                                        )
    def process_df(self, subreddit):
        print('process_df')
        df = pd.DataFrame(self.get_discussion_submissions(subreddit))
        crypto_threads = df[['id','num_comments','created_utc']]
        print('Using df:')
        print(crypto_threads)
        return crypto_threads

    # to get top 15 comments for each day: sort by popularity, 
    def get_comments(self, subreddit):
        print('get_comments')
        gen_topic = Topic.objects.filter(type='gen')[0]
        btc_topic = Topic.objects.filter(type='btc')[0]
        eth_topic = Topic.objects.filter(type='eth')[0]
        df = self.process_df(subreddit)
        data = []
        for i in df.iterrows():
            if Submission.objects.filter(id=i[1].id):
                continue
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
                comment_dict_list.append(comment_dict)
            data.append({
                'id': i[1].id,
                'post_date': datetime.utcfromtimestamp(i[1].created_utc).strftime('%Y-%m-%d'),
                'comments': comment_dict_list
            })
        print('data dict:')
        return data

    def append_data(self, subreddit):
        print('append_data')
        for i in self.get_comments(subreddit):
            submission = Submission(date=i['post_date'], id=i['id'], subreddit=subreddit)
            submission.save()
            for j in i['comments']:
                comment = Comment(id=j['id'],text=j['text'], score=j['score'], date=j['date'], submission=submission)
                comment.save()
                comment.topic.add(*j['topic'])

    def handle(self, *args, **options):
        try:
            self.append_data('bitcoin')
            self.append_data('cryptocurrency')
            self.append_data('ethtrader')
            print('Success!')
        except:
            raise CommandError('An error has occurred.')

# def main():
#     append_data()
#     print('Job done!')
# if __name__ == '__main__':
#     main()
