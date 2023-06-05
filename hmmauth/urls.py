from django.urls import path,include
from hmmauth import views
urlpatterns = [
    path('', views.welcomeView, name='welcomeView'),
    path('hospital_login', views.hospital_loginView, name='hospital_loginView'),
    path('register_hospital', views.register_loginView, name='register_loginView'),
    path('create_hospital_account', views.create_hospital_accountView, name='create_hospital_accountView'),
    path('hospital_login_', views.hospital_login_View, name='hospital_login_View'),
    path('logout', views.logoutView, name='logoutView'),
]


