import praw
from pmaw import PushshiftAPI
import pandas as pd
from datetime import datetime
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

    def bearer_oauth(self, r):
        r.headers[
            "Authorization"
        ] = f"Bearer AAAAAAAAAAAAAAAAAAAAAH9vdgEAAAAA3HOPmlZsRmcW6nfSCOx9cCgscLc%3DPU9hTkTbmFfzA2hAzKA6CGQWmuzLZ3k6alGkrXOzrSQo4lvLvL"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def connect_to_endpoint(self, url, params):
        response = requests.get(url, auth=self.bearer_oauth, params=params)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    def generate_query(self, topic):
        if topic == "btc":
            return {
                "query": "(btc OR bitcoin) -giveaway",
                "tweet.fields": "public_metrics,created_at",
                "max_results": 100,
                "sort_order": "relevancy",
            }
        elif topic == "eth":
            return {
                "query": "(eth OR ethereum) -giveaway",
                "tweet.fields": "public_metrics,created_at",
                "max_results": 100,
                "sort_order": "relevancy",
            }
        else:
            return {
                "query": "(crypto OR cryptocurrency OR blockchain) -giveaway",
                "tweet.fields": "public_metrics,created_at",
                "max_results": 100,
                "sort_order": "relevancy",
            }

    def paginate(self, topic, next_token=None):
        # print(2)
        if not next_token:
            search_url = "https://api.twitter.com/2/tweets/search/recent"
        else:
            search_url = (
                "https://api.twitter.com/2/tweets/search/recent?pagination_token="
                + next_token
            )
        query_params = self.generate_query(topic)
        # print(3)
        json_response = self.connect_to_endpoint(search_url, query_params)
        # print(4)
        return json_response

    def gather_tweets(self, topic, num_tweets):
        response = self.paginate(topic)
        tweets = response["data"]
        next_token = response["meta"]["next_token"]
        while len(tweets) <= num_tweets:
            response = self.paginate(topic, next_token)
            next_token = response["meta"]["next_token"]
            for i in response["data"]:
                if i["public_metrics"]["like_count"] > 100:
                    tweets.append(i)
        return tweets

    def save_tweets(self, topic):
        tweets = self.gather_tweets(topic, 200)
        for tweet in tweets:
            if not Tweet.objects.filter(tweet_id=tweet["id"]):
                new_tweet = Tweet(
                    id=tweet["id"],
                    date=datetime.strptime(tweet["created_at"][:-14], "%Y-%m-%d"),
                    topic=Topic.objects.filter(type=topic),
                    likes=tweet["public_metrics"]["like_count"],
                    retweets=tweet["public_metrics"]["retweet_count"],
                    text=tweet["text"],
                )
                new_tweet.save()
            else:
                print("Tweet already exists")

    # Run the script for list of subreddits
    def handle(self, *args, **options):
        try:
            self.gather_tweets("btc", 200)
            self.gather_tweets("eth", 200)
            self.gather_tweets("gen", 200)

            print("Success!")
        except:
            raise CommandError("An error has occurred.")
