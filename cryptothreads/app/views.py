from django.shortcuts import render, redirect
from django.views.generic import RedirectView
from .models import Submission, Comment, Topic, TradingDay
from datetime import datetime

def convert_timeframes(timeframe):
    index=0
    if timeframe=='year':
        index = 365
    elif timeframe=='month':
        index = 30
    elif timeframe=='week':        
        index = 7
    return index

# Create your views here.
def timeframe(request, timeframe, asset):
    index = 0
    trading_days = list(TradingDay.objects.all()[800:])
    index = convert_timeframes(timeframe)
    url = 'app/{0}-chart.html'.format(asset)
    print(index)
    return render(request, url, {
        'qs': trading_days[-index:]
    })    

def date(request, timeframe='all', timestamp='', asset='total'):
    date = datetime.utcfromtimestamp(int(float(timestamp)))
    date = date.strftime('%Y-%m-%d')
    submissions = list(Submission.objects.filter(date=date))
    comments_c,comments_b,comments_e = [],[],[]
    url = 'app/{0}-chart.html'.format(asset)
    found_post = False
    index = convert_timeframes(timeframe)
    if submissions:
        comments = []
        found_post = True
        for submission in submissions: 
            if submission.subreddit == 'cryptocurrency':
                if asset == 'total':
                    for c in Comment.objects.filter(submission=submission):
                        comments_c.append(c)
                else:
                    for c in Comment.objects.filter(topic__type=asset,submission=submission):
                        comments_c.append(c)
            elif submission.subreddit == 'ethtrader':
                if asset == 'total':
                    for c in Comment.objects.filter(submission=submission):
                        comments_e.append(c)
                else:
                    for c in Comment.objects.filter(topic__type=asset,submission=submission):
                        comments_e.append(c)
            else:
                if asset == 'total':
                    for c in Comment.objects.filter(submission=submission):
                        comments_b.append(c)
                else:
                    for c in Comment.objects.filter(topic__type=asset,submission=submission):
                        comments_b.append(c)

    return render(request, url, {
        'qs': list(TradingDay.objects.all())[-index:],
        'comments_c': comments_c,
        'comments_b': comments_b,
        'comments_e': comments_e,
        'submissions': submissions,
        'timestamp': timestamp,
        'found_post': found_post
    })    

def index(request,asset='total'):
    comments, submissions = '',''
    return render(request, 'app/{0}-chart.html'.format(asset), {
        'qs': list(TradingDay.objects.all()[800:]),
        'comments': comments,
        'submissions': submissions
    })

def base(request):
    return index(request)

class LoginRedirectView(RedirectView):
    pattern_name = 'redirect'
    def get_redirect_url(self, *args, **kwargs):
        return '/chart/total/all'