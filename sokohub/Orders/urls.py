from django.urls import path
from .views import create_order, add_product_to_order, list_my_orders, vendor_order_items, get_order_items, get_user_active_orders_json

urlpatterns = [
    path("", create_order, name="create_order"),
    path("add_order_item/", add_product_to_order, name="add_order_item"),
    path("my_orders/", list_my_orders, name="my_orders"), # for customer
    path("vendor_orders/", vendor_order_items, name="vendor-order-items"),
    path("order_items/", get_order_items, name="order_items"), #Customer
    path('active_orders/', get_user_active_orders_json, name="get_active_orders_json")  #customer
]