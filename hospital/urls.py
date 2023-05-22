from django.urls import path,include
from hospital import views

urlpatterns = [
    path('hospital_dashboard', views.hospital_dashboardView, name='hospital_dashboardView'),
    
    
    path('department', views.departmentView, name='departmentView'),
    path('add_department', views.add_departmentView, name='add_departmentView'),
    path('save_add_department', views.save_add_departmentView, name='save_add_departmentView'),
    path('edit_department/<str:departmentid>', views.edit_departmentView, name='edit_departmentView'),
    path('update_department/<str:departmentid>', views.update_departmentView, name='update_departmentView'),
    path('delete_department/<str:departmentid>', views.delete_departmentView, name='delete_departmentView'),
    
    
    path('add_doctor', views.add_doctorView, name='add_doctorView'),
    path('doctor_list', views.doctor_listView, name='doctor_listView'),
    path('create_doctor', views.create_doctorView, name='create_doctorView'),

    
    path('add_patient', views.add_patientView, name='dd_patientView'),
    path('patient_list', views.patient_listView, name='patient_listView'),
    path('create_patient', views.create_patientView, name='create_patientView'),


    path('add_humanresource', views.add_humanresourceView, name='add_humanresourceView'),
    path('create_humanresource', views.create_humanresourceView, name='create_humanresourceView'),
    path('humanresource_list', views.humanresource_listView, name='humanresource_listView'),


    path('add_appointment', views.add_appointmentView, name='add_appointmentView'),
    path('create_appointment', views.create_appointmentView, name='create_appointmentView'),
    path('appointment_list', views.appointment_listView, name='appointment_listView'),


]


