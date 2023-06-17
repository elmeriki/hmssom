from django.urls import path,include
from finance import views

urlpatterns = [
    path('add_payment/<str:patien_id>', views.add_paymentView, name='add_paymentView'),
    path('payment_list', views.payment_listView, name='payment_listView'),
    path('paymentcategory', views.paymentcategoryView, name='paymentcategoryView'),
    path('add_paymentcategory', views.add_paymentcategoryView, name='add_paymentcategoryView'),
    path('add_expense', views.add_expenseView, name='add_expenseView'),
    path('expense_list', views.expense_listView, name='expense_listView'),
    path('expensecategory', views.expensecategoryView, name='expensecategoryView'),
    path('add_expensecategory', views.add_expensecategoryView, name='add_expensecategoryView'),

    path('create_new_category', views.create_new_categoryView, name='create_new_categoryView'),

    path('create_new_expenses', views.create_new_expensesView, name='create_new_expensesView'),

    path('create_new_payment_category', views.create_new_payment_categoryView, name='create_new_payment_categoryView'),
    
    path('record_payment', views.record_paymentView, name='record_paymentView'),


]
