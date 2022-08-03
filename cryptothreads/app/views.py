from django.shortcuts import render
from django.views.generic import RedirectView
from .models import Submission, Comment, TradingDay, Tweet
from datetime import datetime
from django.http import JsonResponse

# Convert timeframes dictionary
TIMEFRAME_DICT = {"all": 0, "year": 365, "month": 30, "week": 7}

# Timeframe view given asset
def timeframe(request, timeframe, asset):
    index = 0
    trading_days = list(TradingDay.objects.all()[800:])
    index = TIMEFRAME_DICT[timeframe]
    url = "app/{0}-chart.html".format(asset)
    if request.GET.get("timestamp"):
        timestamp = request.GET.get("timestamp")
        comments = []
        date = datetime.utcfromtimestamp(int(float(timestamp)))
        date = date.strftime("%Y-%m-%d")
        submissions = list(Submission.objects.filter(date=date))
        if submissions:
            for submission in submissions:
                if asset == "total":
                    for c in Comment.objects.filter(submission=submission):
                        comments_dict = {
                            "comment_obj": c,
                            "subreddit": c.submission.subreddit,
                        }
                        comments.append(comments_dict)
        data = {"submissions": submissions, "comments": comments}
        return JsonResponse(data)
    return render(request, url, {"qs": trading_days[-index:]})


def prepare_tweet_dict(tweets):
    tweet_dict_list = []
    for tweet in tweets[0:50]:
        tweet_dict_list.append(
            {
                "date": tweet.date,
                "id": tweet.id,
                "likes": tweet.likes,
                "retweets": tweet.retweets,
                "text": tweet.text,
            }
        )
    return tweet_dict_list


# AJAX view returns comments and submissions given a get request's timestamp
def date(request):
    if request.method == "GET":
        # Get URL params
        timestamp = request.GET.get("timestamp")
        asset = request.GET.get("asset")
        date = datetime.utcfromtimestamp(int(float(timestamp))).strftime("%Y-%m-%d")
        submissions = list(Submission.objects.filter(date=date))
        comments_arr = []
        submissions_dict_list = []
        if submissions:
            for submission in submissions:
                submission_dict = {
                    "date": submission.date,
                    "id": submission.id,
                    "subreddit": submission.subreddit,
                }
                if asset == "total":
                    comments = Comment.objects.filter(submission=submission)
                    submissions_dict_list.append(submission_dict)
                    tweets = prepare_tweet_dict(list(Tweet.objects.filter(date=date)))
                else:
                    comments = Comment.objects.filter(
                        topic__type=asset, submission=submission
                    )
                    tweets = prepare_tweet_dict(
                        list(Tweet.objects.filter(topic__type=asset, date=date))
                    )
                    if comments:
                        submissions_dict_list.append(submission_dict)
                        print(submission_dict)
                    else:
                        continue
                for c in comments:
                    comments_dict = {
                        "text": c.text,
                        "score": c.score,
                        "subreddit": c.submission.subreddit,
                    }
                    comments_arr.append(comments_dict)
            comments_arr = sorted(comments_arr, key=lambda x: x["score"], reverse=True)
            data = {
                "submissions": submissions_dict_list,
                "comments": comments_arr,
                "tweets": tweets,
            }
            if len(submissions_dict_list) > 0:
                return JsonResponse(data, status=200)
            else:
                return JsonResponse({}, status=400)


def index(request, asset="total"):
    return render(
        request,
        "app/{0}-chart.html".format(asset),
        {
            "qs": list(TradingDay.objects.all()[800:]),
        },
    )


# Redirect users on base url to specified url
class LoginRedirectView(RedirectView):
    pattern_name = "redirect"

    def get_redirect_url(self, *args, **kwargs):
        return "/chart/total/all"
