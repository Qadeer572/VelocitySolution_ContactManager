from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('contact/',views.myContact, name='contact'),
    path('', views.dashboard, name='dashboard'),
]