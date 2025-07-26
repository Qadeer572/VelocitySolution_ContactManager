from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('contact/',views.myContact, name='contact'),
    path('', views.dashboard, name='dashboard'),
    path('add_contact/', views.addContact, name='add_contact'),
    path('update_contact/<int:contact_id>/', views.updateContact, name='update_contact'),
]