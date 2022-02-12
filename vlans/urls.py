from django.urls import path 
from . import views

urlpatterns = [
    path('list_vlans',views.list_vlans, name='list_vlans'),
    path('create_vlan',views.create_vlan, name='create_vlan')
]