from django.urls import path,include
from finance import views

urlpatterns = [
    path('add_payment', views.add_paymentView, name='add_paymentView'),
    path('payment_list', views.payment_listView, name='payment_listView'),
    path('draft_payment', views.draft_payment_listView, name='draft_payment_listView'),

  

]
