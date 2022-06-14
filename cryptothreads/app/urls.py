from django.urls import path

from . import views

urlpatterns = [
    path('test', views.test, name='test'),
    # path('', views.ChartView.as_view(), name='index'),
    path('<str:asset>', views.index, name='index'),
    # path('date/<str:date>', views.date, name='date'),
    # path('<str:tf>', views.index, name='tf'),
    path('<str:asset>/<str:timestamp>', views.date, name='date'),
]