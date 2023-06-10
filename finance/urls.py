from django.urls import path,include
from finance import views

urlpatterns = [
    path('add_payment', views.add_paymentView, name='add_paymentView'),
    path('payment_list', views.payment_listView, name='payment_listView'),
  

]
