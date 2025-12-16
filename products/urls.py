from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    
    path('vendor/products/add/', views.add_product, name='add_product'),
    path('vendor/products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('vendor/products/', views.vendor_product_list, name='vendor_product_list'),
    path('vendor/products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    
    path('vendor/category/add/', views.add_category, name='add_category'),
    path('vendor/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('vendor/category/', views.vendor_category_list, name='vendor_category_list'),
    path('vendor/category/delete/<int:pk>/', views.delete_category, name='delete_category'),  
]
