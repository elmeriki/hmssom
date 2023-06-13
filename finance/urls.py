from django.urls import path,include
from finance import views

urlpatterns = [
    path('add_payment', views.add_paymentView, name='add_paymentView'),
    path('payment_list', views.payment_listView, name='payment_listView'),
    path('edit_payment/<str:paymentid>', views.edit_paymentView, name='edit_paymentView'),
    path('update_payment/<str:paymentid>', views.update_paymentView, name='update_paymentView'),
    path('delete_payment/<str:paymentid>', views.delete_paymentView, name='delete_paymentView'),


    path('paymentcategory', views.paymentcategoryView, name='paymentcategoryView'),
    path('add_paymentcategory', views.add_paymentcategoryView, name='add_paymentcategoryView'),
    path('edit_paymentcategory/<str:paymentcategoryid>', views.edit_paymentcategoryView, name='edit_paymentcategoryView'),
    path('update_paymentcategory/<str:paymentcategoryid>', views.update_paymentcategoryView, name='update_paymentcategoryView'),
    path('delete_paymentcategory/<str:paymentcategoryid>', views.delete_paymentcategoryView, name='delete_paymentcategoryView'),


    path('add_expense', views.add_expenseView, name='add_expenseView'),
    path('expense_list', views.expense_listView, name='expense_listView'),
    path('expensecategory', views.expensecategoryView, name='expensecategoryView'),
    path('add_expensecategory', views.add_expensecategoryView, name='add_expensecategoryView'),

    path('create_new_category', views.create_new_categoryView, name='create_new_categoryView'),

    path('create_new_expenses', views.create_new_expensesView, name='create_new_expensesView'),

    path('create_new_payment_category', views.create_new_payment_categoryView, name='create_new_payment_categoryView'),
    
    path('record_payment', views.record_paymentView, name='record_paymentView'),


]
