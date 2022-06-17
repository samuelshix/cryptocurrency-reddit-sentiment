from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.base, name='base'),
    # path('test', views.test, name='test'),
    path('<str:asset>', views.index, name='index'),
    # path('date/<str:date>', views.date, name='date'),
    # path('<str:tf>', views.index, name='tf'),
    # path('<str:asset>/<str:timestamp>', views.date, name='date'),
    path('<str:asset>/<str:timeframe>', views.timeframe, name='timeframe'),
    path('<str:asset>/<str:timeframe>/<str:timestamp>', views.date, name='timeframe'),
    # path('<path:path>/<str:timeframe>', views.date, name='timeframe'),

]