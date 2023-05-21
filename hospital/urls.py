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
    path('doctor', views.doctorView, name='doctorView'),
    path('doctor_list', views.doctor_listView, name='doctor_listView'),
    
    path('patient_list', views.patient_listView, name='patient_listView'),


]
