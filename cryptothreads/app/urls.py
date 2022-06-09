from django.urls import path

from . import views

urlpatterns = [
    # path('', views.ChartView.as_view(), name='index'),
    path('', views.index, name='index'),
    path('btc/', views.btc, name='btc'),
    path('eth/', views.eth, name='eth'),
]