import praw
from pmaw import PushshiftAPI
import pandas as pd
from datetime import datetime


api = PushshiftAPI()

gen = api.search_submissions(user = 'AutoModerator',
                             title = 'daily discussion',
                             subreddit = 'superstonk',
                             num_comments = '>500',
                             limit = 1000
                             
    )

df = pd.DataFrame(gen)
df[["created_utc"]] = df[["created_utc"]].apply(pd.to_datetime, unit='s')

df['created_utc'] = df['created_utc'].dt.date


superstonk = df[['id','num_comments','upvote_ratio','created_utc']]