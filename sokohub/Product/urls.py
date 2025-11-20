from django.urls import path
from .views import create_product, get_my_products, get_all_products, vendor_add_products
urlpatterns = [
    path('create/', create_product, name = 'add_product'),
    path('my_products/', get_my_products, name = 'vendor_products'),
    path('add_products/', vendor_add_products, name = 'vendor_add_products'),
]