from django.contrib import admin
from app.models import Submission, Comment, Topic, TradingDay, Tweet

admin.site.register(Submission)
admin.site.register(Comment)
admin.site.register(Topic)
admin.site.register(TradingDay)
admin.site.register(Tweet)
