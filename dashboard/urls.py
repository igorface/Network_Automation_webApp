from django.urls import path 
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('vlans_list',views.vlans_list, name='vlans_list'),
    path('admin',views.index,name='admin'),
]