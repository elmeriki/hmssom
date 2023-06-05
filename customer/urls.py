from django.urls import path,include
from customer import views

urlpatterns = [
    path('add_medicine', views.add_medicineView, name='add_medicineView'),
    path('create_medicine', views.create_medicineView, name='create_medicineView'),
    path('medicine_list', views.medicine_listView, name='prescriptions_listView'),
    path('medicine_by_category/<str:category>', views.medicine_by_categoryView, name='medicine_by_categoryView'),


    path('add_prescription', views.add_prescriptionView, name='add_prescriptionView'),
    path('create_prescription', views.create_prescriptionView, name='create_prescriptionView'),
    path('prescription_list', views.prescription_listView, name='prescription_listView'),


    path('add_appointment', views.add_appointmentView, name='add_appointmentView'),
    path('create_appointment', views.create_appointmentView, name='create_appointmentView'),
    path('appointment_list', views.appointment_listView, name='appointment_listView'),


]
