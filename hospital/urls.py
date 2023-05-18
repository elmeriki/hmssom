from django.urls import path,include
from hospital import views

urlpatterns = [
    path('patient_list', views.patient_listView, name='patient_listView'),
    path('hospital_dashboard', views.hospital_dashboardView, name='hospital_dashboardView'),

]
