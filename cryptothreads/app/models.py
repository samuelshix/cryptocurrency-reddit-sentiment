from django.db import models

# Create your models here.
class Submission(models.Model):
    id = models.TextField(max_length=20, primary_key=True)
    date = models.DateField()

class Topic(models.Model):
    type = models.CharField(max_length = 3)

class Comment(models.Model):
    id = models.TextField(max_length=20, primary_key=True)
    text = models.CharField(max_length=10000)
    score = models.IntegerField()
    date = models.DateField()
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    topic = models.ManyToManyField(Topic, related_name='topics')

# class Eth_Comment():
#     id = models.TextField(max_length=20, primary_key=True)
#     text = models.CharField(max_length=10000)
#     score = models.IntegerField()
#     date = models.DateField()
#     submission = models.ForeignKey(Submission, on_delete=models.CASCADE)

# class Btc_Comment():
#     id = models.TextField(max_length=20, primary_key=True)
#     text = models.CharField(max_length=10000)
#     score = models.IntegerField()
#     date = models.DateField()
#     submission = models.ForeignKey(Submission, on_delete=models.CASCADE)

class TradingDay(models.Model):
    date = models.DateField()
    crypto_cap = models.IntegerField()
    ethereum_price = models.IntegerField()
    bitcoin_price = models.IntegerField()
    # comments = models.ForeignKey(Comment)
