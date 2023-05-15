from django.urls import path,include
from hmmauth import views

urlpatterns = [
    path('', views.welcomeView, name='welcomeView'),
]


