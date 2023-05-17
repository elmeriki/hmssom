from django.urls import path,include
from hmmauth import views

urlpatterns = [
    path('', views.welcomeView, name='welcomeView'),
    path('hospital_login', views.hospital_loginView, name='hospital_loginView'),
    path('register_hospital', views.register_loginView, name='register_loginView'),

]


