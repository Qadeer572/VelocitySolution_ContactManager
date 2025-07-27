from django.contrib import admin
from django.urls import path
from . import views
from contact.views import export_catagory_pdf
urlpatterns = [
    path('contact/',views.myContact, name='contact'),
    path('', views.dashboard, name='dashboard'),
    path('add_contact/', views.addContact, name='add_contact'),
    path('update_contact/<int:contact_id>/', views.updateContact, name='update_contact'),
    path('delete_contact/<int:contact_id>/', views.deleteContact, name='delete_contact'),
    path('catagoryContact/',views.catagoryContact, name='catagoryContact'),
    path('exportCatagoryContact/', views.exportCatagoryContact, name='exportCatagoryContact'),
    path('export-category-pdf/', export_catagory_pdf, name='export_category_pdf'),
]