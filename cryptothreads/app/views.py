from django.shortcuts import render, redirect
from django.views.generic import TemplateView
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
    subreddits = []
    url = 'app/{0}-chart.html'.format(asset)
    found_post = False
    index = convert_timeframes(timeframe)
    if submissions:
        comments = []
        found_post = True
        for submission in submissions: 
            subreddits.append(submission.subreddit)
            if asset == 'total':
                for c in Comment.objects.filter(submission=submission):
                    comments.append(c)
            else:
                for c in Comment.objects.filter(topic__type=asset,submission=submission):
                    comments.append(c)
    else:
        comments = ''
    return render(request, url, {
        'qs': list(TradingDay.objects.all())[-index:],
        'comments': comments,
        'submissions': submissions,
        'timestamp': timestamp,
        'found_post': found_post,
        'subreddits': subreddits
        # 'date': date
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

# def timeframe(request, asset, timeframe):
#     timestamp, submissions = '',''
#     if len(path) > 1:
#         args = path.split('/')[1:]
#         for i in args:
#     date = datetime.utcfromtimestamp(int(float(timestamp)))
#     date = date.strftime('%Y-%m-%d')
#     submissions = list(Submission.objects.filter(date=date, subreddit='cryptocurrency'))
#     # submissions.append(Submission.objects.filter(date=date, subreddit='ethtrader'))
#     # submissions.append(Submission.objects.filter(date=date, subreddit='bitcoin'))
#     url = 'app/{0}-chart.html'.format(asset)
#     found_post = False
#     if submissions:
#         found_post = True
#         if asset == 'total':
#             comments = list(Comment.objects.filter(submission=submissions[0]))
#         elif asset == 'btc':
#             comments = list(Comment.objects.filter(topic__type='btc',submission=submissions[0]))
#         elif asset == 'eth':
#             comments = list(Comment.objects.filter(topic__type='eth',submission=submissions[0]))
#     else:
#         comments = ''
#     print(found_post)
#     return render(request, url, {
#         'qs': list(TradingDay.objects.all()[800:]),
#         'comments': comments,
#         'submissions': submissions,
#         'timestamp': timestamp,
#         'found_post': found_post
#         # 'date': date
#     })    

# def daily(request):

# def eth(request):

# class ChartView(TemplateView):
#     template_name = 'app/chart.html'

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['qs'] = TradingDay.objects.all()[2478:]
#         ctx['comments'] = Comment.objects.all()
#         # for comment in ctx['comments']:

#         return ctx