from django.db import models
import praw
from pmaw import PushshiftAPI
import pandas as pd
from datetime import datetime

# Create your models here.
class Submission(models.Model):
    date = models.DateField()

class Comment(models.Model):
    text = models.CharField(max_length=10000)
    score = models.IntegerField()
    date = models.DateField()
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)