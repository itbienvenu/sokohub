from django.urls import path
from .views import create_product
urlpatterns = [
    path('', create_product, name = 'add_product'),
    # path('list/', list_product, name = 'list-product')
]