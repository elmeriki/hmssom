from django.urls import path,include
from administrator import views

urlpatterns = [
    path('delete_curency/<str:id>', views.delete_curencyView, name='delete_curencyView'),
    path('add_curency_list', views.add_curency_listView, name='add_curency_listView'),
    path('add_curency', views.add_curencyView, name='add_curencyView'),
    path('create_curency', views.create_curencyView, name='create_curencyView'),

    path('region_list', views.region_listView, name='region_listView'),
    path('add_region', views.add_regionView, name='add_regionView'),
    path('create_region', views.create_regionView, name='create_regionView'),
    path('delete_region/<str:id>', views.delete_regionView, name='delete_regionView'),

]
