from django.urls import path
from .views import create_order, add_product_to_order

urlpatterns = [
    path("", create_order, name="create_order"),
    path("add_order_item/", add_product_to_order, name="add_order_item")
]