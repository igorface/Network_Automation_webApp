from django.urls import path 
from . import views

urlpatterns = [
    path('list_vlans',views.list_vlans, name='list_vlans'),
    path('create_vlan',views.create_vlan, name='create_vlan'),
    path('result_of_creating_vlan',views.result_of_creating_vlan, name='result_of_creating_vlan'),
    path('unable_to_connect',views.unable_to_connect, name='unable_to_connect')
]