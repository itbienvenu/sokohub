from django.urls import path
from .views import create_order, add_product_to_order, list_my_orders, list_order_items

urlpatterns = [
    path("", create_order, name="create_order"),
    path("add_order_item/", add_product_to_order, name="add_order_item"),
    path("my_orders/", list_my_orders, name="my_orders"), # for customer
    path("vendor_orders/", list_order_items, name="vendor-order-items")
]