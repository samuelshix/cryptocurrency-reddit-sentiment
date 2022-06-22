from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.LoginRedirectView.as_view(), name='redirect'),
    path('chart/<str:asset>', views.index, name='index'),
    path('chart/<str:asset>/<str:timeframe>/', views.timeframe, name='timeframe'),
    path('get/comment-data/', views.date, name='data'),
]