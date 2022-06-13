from django.urls import path

from . import views

urlpatterns = [
    # path('', views.ChartView.as_view(), name='index'),
    path('', views.index, name='index'),
    # path('date/<str:date>', views.date, name='date'),
    # path('<str:tf>', views.index, name='tf'),
    path('<str:timestamp>', views.datetotal, name='date'),
    path('btc/', views.btc, name='btc'),
    path('btc/<str:timestamp>', views.datebtc, name='datebtc'),
    path('eth/', views.eth, name='eth'),
    path('eth/<str:timestamp>', views.dateeth, name='dateeth'),
    path('info/', views.info, name='info'),
]