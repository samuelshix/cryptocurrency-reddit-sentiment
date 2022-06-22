from django.shortcuts import render, redirect
from django.views.generic import RedirectView
from .models import Submission, Comment, Topic, TradingDay
from datetime import datetime
from django.http import JsonResponse

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
    if request.GET.get('timestamp'):
        timestamp = request.GET.get('timestamp')
        comments = []
        date = datetime.utcfromtimestamp(int(float(timestamp)))
        date = date.strftime('%Y-%m-%d')
        submissions = list(Submission.objects.filter(date=date))
        if submissions:
            for submission in submissions: 
                if asset=='total':
                    for c in Comment.objects.filter(submission=submission):
                        comments_dict = {
                            'comment_obj': c,
                            'subreddit': c.submission.subreddit
                        }
                        comments.append(comments_dict)                
        data = {
            'submissions': submissions,
            'comments': comments
        }
        print(data)
        return JsonResponse(data)
    return render(request, url, {
        'qs': trading_days[-index:]
    })    

def date(request):
    if request.method == 'GET':
        timestamp = request.GET.get('timestamp')
        asset = request.GET.get('asset')
        date = datetime.utcfromtimestamp(int(float(timestamp)))
        date = date.strftime('%Y-%m-%d')
        submissions = list(Submission.objects.filter(date=date))
        relevant_submissions = []
        comments_c,comments_b,comments_e = [],[],[]
        comments_arr = []
        submissions_dict_list = []
        url = f'app/{asset}-chart.html'
        found_post = False
        index = convert_timeframes(timeframe)
        if submissions:
            for submission in submissions: 
                submission_dict = {
                    'date': submission.date,
                    'id': submission.id,
                    'subreddit': submission.subreddit
                }
                # submissions_dict_list.append(submission_dict)
                if asset=='total':
                    comments = Comment.objects.filter(submission=submission)
                    submissions_dict_list.append(submission_dict)
                else:
                    comments = Comment.objects.filter(topic__type=asset,submission=submission)
                    if comments: submissions_dict_list.append(submission_dict)
                for c in comments:
                    comments_dict = {
                        'text': c.text,
                        'score': c.score,
                        'subreddit': c.submission.subreddit
                    }
                    comments_arr.append(comments_dict)
                print(comments)
            comments_arr = sorted(comments_arr, key = lambda x: x['score'], reverse=True)                            
            data = {
                'submissions': submissions_dict_list,
                'comments': comments_arr,
            }
            print(data)
            if len(submissions_dict_list)>0:
                return JsonResponse(data, status=200)
            else:
                return JsonResponse({}, status = 400)


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