
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),


]
