from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Submission, Comment, Topic, TradingDay
import re
# Create your views here.
def index(request):
    comments = list(Comment.objects.all())
    submissions = list(Submission.objects.all())
    # for i in comments:
    #     i.text = re.sub('"',"“", i.text)
    #     i.save()
        # print(i.text)
    # if request.method == "POST": 
    #     comments = list()
    return render(request, 'app/chart.html', {
        'qs': list(TradingDay.objects.all()[2000:]),
        'comments': comments,
        'submissions': submissions
    })

def btc(request):
    comments = list(Comment.objects.filter(topic__type='btc'))
    submissions = list(Submission.objects.all())

    return render(request, 'app/btc-chart.html', {
        'qs': list(TradingDay.objects.all()[800:]),
        'comments': comments,
        'submissions': submissions
    })   

def eth(request):
    comments = list(Comment.objects.filter(topic__type='eth'))
    submissions = list(Submission.objects.all())

    return render(request, 'app/eth-chart.html', {
        'qs': list(TradingDay.objects.all()[800:]),
        'comments': comments,
        'submissions': submissions
    })     

def info(request):
    return render(request,'app/info.html')
# def eth(request):

# class ChartView(TemplateView):
#     template_name = 'app/chart.html'

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['qs'] = TradingDay.objects.all()[2478:]
#         ctx['comments'] = Comment.objects.all()
#         # for comment in ctx['comments']:

#         return ctx