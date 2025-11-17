from django.urls import path
from .views import create_product, get_my_products
urlpatterns = [
    path('', create_product, name = 'add_product'),
    path('my_products/', get_my_products, name = 'my_products')
]