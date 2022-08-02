from django.db import models


class Submission(models.Model):
    id = models.TextField(max_length=20, primary_key=True)
    date = models.DateField()
    subreddit = models.TextField(max_length=20, default="cryptocurrency")


class Topic(models.Model):
    type = models.CharField(max_length=3)


class Tweet(models.Model):
    id = models.TextField(max_length=20, primary_key=True)
    date = models.DateField()
    topic = models.ManyToManyField(Topic, related_name="tweet_topics")
    likes = models.IntegerField(default=0)
    retweets = models.IntegerField(default=0)
    text = models.TextField(max_length=280)


class Comment(models.Model):
    id = models.TextField(max_length=20, primary_key=True)
    text = models.CharField(max_length=10000)
    score = models.IntegerField()
    date = models.DateField()
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    topic = models.ManyToManyField(Topic, related_name="topics")


class TradingDay(models.Model):
    date = models.DateField()
    crypto_cap = models.BigIntegerField()
    ethereum_price = models.IntegerField()
    bitcoin_price = models.IntegerField()
