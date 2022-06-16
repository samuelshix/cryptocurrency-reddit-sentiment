from django.urls import path

from . import views

urlpatterns = [
    path('', views.base, name='index'),
    # path('test', views.test, name='test'),
    path('<str:asset>', views.index, name='index'),
    # path('date/<str:date>', views.date, name='date'),
    # path('<str:tf>', views.index, name='tf'),
    path('<str:asset>/<str:timestamp>', views.date, name='date'),
]