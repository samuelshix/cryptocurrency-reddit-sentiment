import praw
from pmaw import PushshiftAPI
import pandas as pd
from datetime import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test1.settings")

from models import Submission, Comment

from testapp.models import Location

api = PushshiftAPI()
reddit = praw.Reddit(
    client_id="3B_hPuLSNInJTsozWMHqcA",
    client_secret="mMcsjS3apcp-wIxm2mcGNlEaAZsn_A",
    user_agent="web:crypto-comment-sentiment:v1.0.0 (by /u/kash_sam_)",
)

def get_discussion_submissions():
    return api.search_submissions(user = 'CryptoDaily-',
                                title = 'Daily General Discussion',
                                subreddit = 'cryptocurrency',
                                sort = 'desc',
                                limit = 2000                   
    )

def process_df():
    df = pd.DataFrame(get_discussion_submissions())
    # df[["created_utc"]] = df[["created_utc"]].apply(pd.to_datetime, unit='s')
    # df['created_utc'] = df['created_utc'].dt.date
    crypto_threads = df[['id','num_comments','created_utc']]
    return crypto_threads

# to get top 10 for each day on multi-day post: sort by popularity, 
def get_comments():
    df = process_df()
    data = []
    for i in df.iterrows():
        submission = reddit.submission(i[1].id)
        submission.comment_sort = "top"
        comment_dict_list = []
        for top_level_comment in submission.comments[0:10]:
            comment_dict = {
                'text': top_level_comment.body,
                'score': top_level_comment.score, 
                'date': datetime.utcfromtimestamp(top_level_comment.created_utc).strftime('%m-%d-%Y')
                }
            comment_dict_list.append(comment_dict)
        data.append({
            'post_date': datetime.utcfromtimestamp(i[1].created_utc).strftime('%m-%d-%Y'),
            'comments': comment_dict_list
        })
    return data

def append_data():
    for i in get_comments():
        submission = Submission(date=i['post_date'])
        for j in i['comments']:
            comment = Comment(text=j['text'], score=j['score'], date=j['date'], submission=submission)
            comment.save()
        submission.save()

def main():
    append_data()
    print('Job done!')
if __name__ == '__main__':
    main()