from django.urls import path,include
from customer import views

urlpatterns = [
    path('add_medicinecategory', views.add_medicinecategoryView, name='add_medicinecategoryView'),
    path('create_medicinecategory', views.create_medicinecategoryView, name='create_medicinecategoryView'),
    path('medicinecategory_list', views.medicinecategory_listView, name='medicinecategory_listView'),
    #path('medicine_by_category/<str:category>', views.medicine_by_categoryView, name='medicine_by_categoryView'),


    path('add_medicine', views.add_medicineView, name='add_medicineView'),
    path('create_medicine', views.create_medicineView, name='create_medicineView'),
    path('medicine_list', views.medicine_listView, name='prescriptions_listView'),
    #path('medicine_by_category/<str:category>', views.medicine_by_categoryView, name='medicine_by_categoryView'),

    path('add_prescription', views.add_prescriptionView, name='add_prescriptionView'),
    path('create_prescription', views.create_prescriptionView, name='create_prescriptionView'),
    path('prescription_list', views.prescription_listView, name='prescription_listView'),
    path('edit_prescription/<str:prescriptionid>', views.edit_prescriptionView, name='edit_prescriptionView'),
    path('update_prescription/<str:prescriptionid>', views.update_prescriptionView, name='update_prescriptionView'),
    path('delete_prescription/<str:prescriptionid>', views.delete_prescriptionView, name='delete_prescriptionView'),


    path('add_appointment', views.add_appointmentView, name='add_appointmentView'),
    path('add_appointment_/<str:patient_id>', views.add_appointment_View, name='add_appointment_View'),
    path('create_appointment', views.create_appointmentView, name='create_appointmentView'),
    path('appointment_list', views.appointment_listView, name='appointment_listView'),
    path('edit_appointment/<str:appointmentid>', views.edit_appointmentView, name='edit_appointmentView'),
    path('update_appointment/<str:appointmentid>', views.update_appointmentView, name='update_pappointmentView'),
    path('delete_appointment/<str:appointmentid>', views.delete_appointmentView, name='delete_appointmentView'),
    path('todays_appointment_list', views.todays_appointment_listView, name='todays_appointment_listView'),
    path('upcoming_appointment_list', views.upcoming_appointment_listView, name='upcoming_appointment_listView'),
    path('create_patient_appointment', views.create_patient_appointmentView, name='create_patient_appointmentView'),
   
   
    path('app_home', views.app_homeView, name='app_homeView'),
    path('app_login', views.app_loginView, name='app_loginView'),
    path('app_register', views.app_registerView, name='app_registerView'),
    path('app_hospital_list/<str:city_names>', views.app_hospital_listView, name='app_hospital_listView'),
    
    
    path('book_now/<str:hospital_id>', views.book_nowView, name='book_nowView'),
    path('create_book_now/<str:hospital_id>', views.create_book_nowView, name='create_book_nowView'),
    path('app_hospital_detail/<str:hospital_id>', views.app_hospital_detailView, name='app_hospital_detailView'),
    path('app_query_search', views.app_query_searchView, name='app_query_searchView'),

]
