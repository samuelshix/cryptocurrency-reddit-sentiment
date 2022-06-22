from django.shortcuts import render
from django.views.generic import RedirectView
from .models import Submission, Comment, TradingDay
from datetime import datetime
from django.http import JsonResponse

# Convert timeframes dictionary
TIMEFRAME_DICT = {
    'all': 0,
    'year': 365,
    'month': 30,
    'week': 7
}

# Timeframe view given asset
def timeframe(request, timeframe, asset):
    index = 0
    trading_days = list(TradingDay.objects.all()[800:])
    index = TIMEFRAME_DICT[timeframe]
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

# ajax view returns comments and submissions given a get request's timestamp
def date(request):
    if request.method == 'GET':
        timestamp = request.GET.get('timestamp')
        asset = request.GET.get('asset')
        date = datetime.utcfromtimestamp(int(float(timestamp))).strftime('%Y-%m-%d')
        submissions = list(Submission.objects.filter(date=date))
        comments_arr = []
        submissions_dict_list = []
        if submissions:
            for submission in submissions: 
                submission_dict = {
                    'date': submission.date,
                    'id': submission.id,
                    'subreddit': submission.subreddit
                }
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
            comments_arr = sorted(comments_arr, key = lambda x: x['score'], reverse=True)                            
            data = {
                'submissions': submissions_dict_list,
                'comments': comments_arr,
            }
            if len(submissions_dict_list)>0:
                return JsonResponse(data, status=200)
            else:
                return JsonResponse({}, status = 400)

def index(request,asset='total'):
    return render(request, 'app/{0}-chart.html'.format(asset), {
        'qs': list(TradingDay.objects.all()[800:]),
    })

# redirect users on base url to specified url
class LoginRedirectView(RedirectView):
    pattern_name = 'redirect'
    def get_redirect_url(self, *args, **kwargs):
        return '/chart/total/all'