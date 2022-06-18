from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.LoginRedirectView.as_view(), name='redirect'),
    # path('test', views.test, name='test'),
    path('chart/<str:asset>', views.index, name='index'),
    # path('date/<str:date>', views.date, name='date'),
    # path('<str:tf>', views.index, name='tf'),
    # path('<str:asset>/<str:timestamp>', views.date, name='date'),
    path('chart/<str:asset>/<str:timeframe>', views.timeframe, name='timeframe'),
    path('chart/<str:asset>/<str:timeframe>/<str:timestamp>', views.date, name='timeframe'),
    # path('<path:path>/<str:timeframe>', views.date, name='timeframe'),

]