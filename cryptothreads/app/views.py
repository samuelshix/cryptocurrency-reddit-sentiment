from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Submission, Comment, Topic, TradingDay
from datetime import datetime

# Create your views here.
def date(request, timestamp, asset):
    date = datetime.utcfromtimestamp(int(float(timestamp)))
    date = date.strftime('%Y-%m-%d')
    submissions = list(Submission.objects.filter(date=date, subreddit='cryptocurrency'))
    # submissions.append(Submission.objects.filter(date=date, subreddit='ethtrader'))
    # submissions.append(Submission.objects.filter(date=date, subreddit='bitcoin'))
    url = 'app/{0}-chart.html'.format(asset)
    found_post = False
    if submissions:
        found_post = True
        if asset == 'total':
            comments = list(Comment.objects.filter(submission=submissions[0]))
        elif asset == 'btc':
            comments = list(Comment.objects.filter(topic__type='btc',submission=submissions[0]))
        elif asset == 'eth':
            comments = list(Comment.objects.filter(topic__type='eth',submission=submissions[0]))
    else:
        comments = ''
    print(found_post)
    return render(request, url, {
        'qs': list(TradingDay.objects.all()[800:]),
        'comments': comments,
        'submissions': submissions,
        'timestamp': timestamp,
        'found_post': found_post
        # 'date': date
    })    

def index(request,asset):
    comments, submissions = '',''
    return render(request, 'app/{0}-chart.html'.format(asset), {
        'qs': list(TradingDay.objects.all()[800:]),
        'comments': comments,
        'submissions': submissions
    })

def base(request):
    comments, submissions = '',''
    return render(request, 'app/total-chart.html', {
        'qs': list(TradingDay.objects.all()[800:]),
        'comments': comments,
        'submissions': submissions
    })

def test(request):
    return render(request, 'app/test.html')

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