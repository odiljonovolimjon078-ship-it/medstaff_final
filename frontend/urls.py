from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('disease-search/', views.disease_search, name='disease_search'),
    path('hospitals/<int:pk>/delete/', views.hospital_delete, name='hospital_delete'),
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/add/', views.staff_add, name='staff_add'),
    path('staff/<int:pk>/', views.staff_detail, name='staff_detail'),
    path('staff/<int:pk>/edit/', views.staff_edit, name='staff_edit'),
    path('staff/<int:pk>/delete/', views.staff_delete, name='staff_delete'),
    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('hospitals/add/', views.hospital_add, name='hospital_add'),
    path('hospitals/<int:pk>/', views.hospital_detail, name='hospital_detail'),
    path('hospitals/<int:pk>/edit/', views.hospital_edit, name='hospital_edit'),
]
