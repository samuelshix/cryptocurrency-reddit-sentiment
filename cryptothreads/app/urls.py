from django.urls import path

from . import views

urlpatterns = [
    # path('', views.ChartView.as_view(), name='index'),
    path('', views.index, name='index'),
    # path('<str:date>', views.index, name='index'),
    path('<str:timestamp>', views.date, name='date'),
    path('btc/', views.btc, name='btc'),
    path('eth/', views.eth, name='eth'),
    path('info/', views.info, name='info'),
]