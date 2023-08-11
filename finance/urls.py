from django.urls import path,include
from finance import views

urlpatterns = [
    path('add_payment/<str:patien_id>', views.add_paymentView, name='add_paymentView'),
    path('payment_list', views.payment_listView, name='payment_listView'),
    path('paymentcategory', views.paymentcategoryView, name='paymentcategoryView'),
    path('add_paymentcategory', views.add_paymentcategoryView, name='add_paymentcategoryView'),
    path('add_appointment_fees', views.add_appointment_feesView, name='add_appointment_feesView'),
    path('add_expense', views.add_expenseView, name='add_expenseView'),
    path('expense_list', views.expense_listView, name='expense_listView'),
    path('expensecategory', views.expensecategoryView, name='expensecategoryView'),
    path('add_expensecategory', views.add_expensecategoryView, name='add_expensecategoryView'),

    path('admission_fees/<str:patient_id>/<str:price>', views.admission_feesView, name='admission_feesView'),
    path('save_admission_fees', views.save_admission_feesView, name='save_admission_feesView'),

    path('admision_fees', views.admision_feesView, name='admision_feesView'),
    path('create_new_category', views.create_new_categoryView, name='create_new_categoryView'),
    path('create_new_expenses', views.create_new_expensesView, name='create_new_expensesView'),

    path('create_new_payment_category', views.create_new_payment_categoryView, name='create_new_payment_categoryView'),
    
    path('record_payment', views.record_paymentView, name='record_paymentView'),
    path('create_new_appointment_category', views.create_new_appointment_categoryView, name='create_new_appointment_categoryView'),
    path('appointment_category', views.appointment_categoryView, name='appointment_categoryView'),
    path('delete_appointment_payment_category/<str:id>', views.delete_appointment_payment_categoryView, name='delete_appointment_payment_categoryView'),

]
