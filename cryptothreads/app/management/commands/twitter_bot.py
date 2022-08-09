import tweepy
from app.models import Comment
import datetime as dt
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()

    def setup_twitter_api(self):
        oauth1_user_handler = tweepy.OAuth1UserHandler(
            "I0CMGgLkG8vJs8UgZnhDP1Rzw",
            "6g967kmPbuG8u1UjBD50zijCh6xyR9Mkft0FsqsYfMs85vcxEa",
            callback="https://coinmarketcap.com/currencies/samoyedcoin/",
        )

        # access_token, access_token_secret = oauth1_user_handler.get_access_token(
        #     "NTZoHWSBJwomS9ERIh5TfbBL2XyuhBBa"
        # )
        api = tweepy.Client(
            bearer_token="AAAAAAAAAAAAAAAAAAAAAH9vdgEAAAAA3HOPmlZsRmcW6nfSCOx9cCgscLc%3DPU9hTkTbmFfzA2hAzKA6CGQWmuzLZ3k6alGkrXOzrSQo4lvLvL",
            consumer_key="I0CMGgLkG8vJs8UgZnhDP1Rzw",
            consumer_secret="6g967kmPbuG8u1UjBD50zijCh6xyR9Mkft0FsqsYfMs85vcxEa",
            access_token="1461832686239195148-oXIrMkvnbZlwgSyJdrY1jeQzp1IQKo",
            access_token_secret="KXR67xFEj84oYfRstM0K0ZbAslBa6iNCnOaiiq707XIhs",
            return_type=dict,
        )
        return api

    # uses yesterday due to the fact that the bot is run every day at midnight
    def get_top_comment(self):
        yesterday = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
        top_comment_data = Comment.objects.filter(date=yesterday).order_by("-score")[0]
        text = top_comment_data.text
        score = top_comment_data.score
        id = top_comment_data.id
        submission_id = top_comment_data.submission.id
        top_comment = {
            "text": text,
            "score": score,
            "id": id,
            "submission_id": submission_id,  # id of discussion thread
            "subreddit": top_comment_data.submission.subreddit,
        }
        return top_comment

    def post_tweet(self, api, comment):
        header = f"Subreddit: {comment['subreddit']}\n\nScore: {comment['score']}\n\n"
        # extra chars: ellipses: 3, quotes: 2
        chars = 280 - len(header) - 5
        comment_text = f'{header}"{comment["text"]}"'
        # if the comment is too long, create a twitter thread
        if len(comment_text) > 280:
            beginning_text, comment_text = comment_text[:chars], comment_text[chars:]
            print(len(beginning_text))
            id = api.create_tweet(text=beginning_text + "...")["data"]["id"]
            while len(comment_text) > chars:
                comment_text, rest_text = comment_text[:chars], comment_text[chars:]
                id = api.create_tweet(
                    in_reply_to_tweet_id=id,
                    text=comment_text + "...",
                )["data"]["id"]
                comment_text = rest_text

            id = api.create_tweet(in_reply_to_tweet_id=id, text=comment_text)["data"][
                "id"
            ]
        else:
            id = api.create_tweet(text=comment_text)["data"]["id"]
        api.create_tweet(
            text=f"Full discussion: https://www.reddit.com/{comment['submission_id']}",
            in_reply_to_tweet_id=id,
        )

    def handle(self, *args, **options):
        api = self.setup_twitter_api()  # type: tweepy.API
        comment = self.get_top_comment()
        try:
            self.post_tweet(api, comment)
        except Exception as e:
            print(e)
