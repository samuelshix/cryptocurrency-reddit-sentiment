from django.urls import path

from . import views

urlpatterns = [
    # path('', views.ChartView.as_view(), name='index'),
    path('', views.index, name='index'),
    # path('date/<str:date>', views.date, name='date'),
    # path('<str:tf>', views.index, name='tf'),
    path('btc/', views.btc, name='btc'),
    path('eth/', views.eth, name='eth'),
    path('info/', views.info, name='info'),
]