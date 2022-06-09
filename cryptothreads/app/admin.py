from django.contrib import admin
from app.models import Submission, Comment, Topic, TradingDay
# Register your models here.

admin.site.register(Submission)
admin.site.register(Comment)
admin.site.register(Topic)
admin.site.register(TradingDay)