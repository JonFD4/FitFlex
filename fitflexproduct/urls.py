
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
     path('product/<int:product_id>/review/', views.submit_review, name='submit_review'), 
]