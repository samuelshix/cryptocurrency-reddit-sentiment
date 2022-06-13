from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Submission, Comment, Topic, TradingDay
import re
from datetime import datetime

# Create your views here.
def date(request, timestamp, chart_type):
    date = datetime.utcfromtimestamp(int(float(timestamp)))
    date = date.strftime('%Y-%m-%d')
    submissions = list(Submission.objects.filter(date=date))
    if chart_type == 'total':
        url = 'app/chart.html'
    elif chart_type == 'btc':
        url = 'app/btc-chart.html'
    elif chart_type == 'eth':
        url = 'app/eth-chart.html'
    found_post = False
    if submissions:
        found_post = True
        if chart_type == 'total':
            comments = list(Comment.objects.filter(submission=submissions[0]))
        elif chart_type == 'btc':
            comments = list(Comment.objects.filter(topic__type='btc',submission=submissions[0]))
        elif chart_type == 'eth':
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

def datetotal(request, timestamp):
    return date(request, timestamp, 'total')   

def datebtc(request, timestamp):
    return date(request, timestamp, 'btc')   

def dateeth(request, timestamp):
    return date(request, timestamp, 'eth')   
   
def index(request):
    comments, submissions = '',''
    if request.method == "POST": 
        if request.POST.get('data'):
            date = request.POST.get('data')
            print(date)
            return redirect('date', timestamp=date)
    return render(request, 'app/chart.html', {
        'qs': list(TradingDay.objects.all()[800:]),
        'comments': comments,
        'submissions': submissions
    })

def btc(request):
    comments, submissions = '',''
    return render(request, 'app/btc-chart.html', {
        'qs': list(TradingDay.objects.all()[800:]),
        'comments': comments,
        'submissions': submissions
    })   

def eth(request):
    comments, submissions = '',''
    return render(request, 'app/eth-chart.html', {
        'qs': list(TradingDay.objects.all()[800:]),
        'comments': comments,
        'submissions': submissions
    })     

def info(request):
    return render(request,'app/info.html')

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