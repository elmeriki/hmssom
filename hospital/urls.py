from django.urls import path,include
from hospital import views

urlpatterns = [
    path('patient_list', views.patient_listView, name='patient_listView'),
    path('hospital_dashboard', views.hospital_dashboardView, name='hospital_dashboardView'),
    path('department_create', views.department_createView, name='department_createView'),
    path('department_list', views.department_listView, name='department_listView'),
    path('department_detail', views.department_detailView, name='department_detailView'),



]
