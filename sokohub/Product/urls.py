from django.urls import path
from .views import list_product
urlpatterns = [
    path('', list_product, name = 'pro1')
]