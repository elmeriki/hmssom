from django.urls import path,include
from hospital import views

urlpatterns = [
    path('patient_list', views.patient_listView, name='patient_listView'),
    path('hospital_dashboard', views.hospital_dashboardView, name='hospital_dashboardView'),
    path('department', views.departmentView, name='departmentView'),
    path('add_department', views.add_departmentView, name='add_departmentView'),
    path('save_add_department', views.save_add_departmentView, name='save_add_departmentView'),
    path('department_update/<int:id>', views.department_updateView, name='department_updateView'),
    path('doctor_list', views.doctor_listView, name='doctor_listView'),


]
