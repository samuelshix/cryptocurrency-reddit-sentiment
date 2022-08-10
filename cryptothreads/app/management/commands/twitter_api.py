import datetime as dt
from app.models import Tweet, Topic
from django.core.management.base import BaseCommand, CommandError
import requests
import os

# Django Command class for custom manage.py commands
class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()

        # self.token = os.environ.get("TWITTER_TOKEN")
        # self.user_agent = os.environ.get("TWITTER_USER_AGENT")
        # Method required by bearer token authentication.

    def n_days_ago(self, days):
        return dt.datetime.now() - dt.timedelta(days=days)

    def bearer_oauth(self, r):
        r.headers["Authorization"] = f"Bearer {os.environ.get('TWITTER_TOKEN')}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def connect_to_endpoint(self, url, params):
        response = requests.get(url, auth=self.bearer_oauth, params=params)
        if response.status_code != 200:
            print("Error: " + str(response.status_code))
            raise Exception(response.status_code, response.text)
        print("Connected to endpoint!")
        return response.json()

    def generate_query(self, topic, days):
        print(f"Days ago: {days}")
        formatted_date = self.n_days_ago(days)
        query_mapping = {
            "btc": "(btc OR bitcoin) -giveaway",
            "eth": "(eth OR ethereum) -giveaway",
            "gen": "(crypto OR cryptocurrency OR blockchain) -giveaway",
        }
        query = {
            "q": query_mapping[topic],
            "count": "100",
            "result_type": "popular",
            "until": str(formatted_date)[0:11],
        }
        return query

    def gather_tweets(self, topic, days):
        search_url = "https://api.twitter.com/1.1/search/tweets.json"
        query_params = self.generate_query(topic, days)
        response = self.connect_to_endpoint(search_url, query_params)
        tweets = response["statuses"]
        return tweets

    def save_tweets(self, topic, days):
        tweets = self.gather_tweets(topic, days)
        topic_obj = Topic.objects.filter(type=topic)[0]
        print(f"Number of tweets found: {len(tweets)}")
        for tweet in tweets:
            if not Tweet.objects.filter(id=tweet["id"]):
                new_tweet = Tweet(
                    id=tweet["id"],
                    date=dt.datetime.strptime(
                        tweet["created_at"], "%a %b %d %H:%M:%S %z %Y"
                    ),
                    likes=tweet["favorite_count"],
                    retweets=tweet["retweet_count"],
                    text=tweet["text"],
                )
                new_tweet.save()
                new_tweet.topic.add(topic_obj)
            else:
                new_tweet = Tweet.objects.filter(id=tweet["id"])[0]
                if topic_obj not in new_tweet.topic.all():
                    new_tweet.topic.add(topic_obj)

    def save_last_week_tweets(self):
        for i in range(0, 7):
            self.save_tweets("btc", i)
            self.save_tweets("eth", i)
            self.save_tweets("gen", i)

    def save_yesterday_tweets(self):
        self.save_tweets("btc", 1)
        self.save_tweets("eth", 1)
        self.save_tweets("gen", 1)
        self.save_tweets("btc", 0)
        self.save_tweets("eth", 0)
        self.save_tweets("gen", 0)

    # Run the script for list of subreddits
    def handle(self, *args, **options):
        try:
            # self.save_last_week_tweets()
            self.save_yesterday_tweets()
            print("Success!")
        except:
            raise CommandError("An error has occurred.")
