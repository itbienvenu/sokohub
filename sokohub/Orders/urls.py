from django.urls import path
from .views import create_order, add_product_to_order, list_my_orders, vendor_order_items, get_order_items, get_user_active_orders_json, cancel_order, delete_order, delete_order_item, update_order_item_quantity








urlpatterns = [
    path("", create_order, name="create_order"),
    path("add_order_item/", add_product_to_order, name="add_order_item"),
    path("my_orders/", list_my_orders, name="my_orders"), # for customer
    path("vendor_orders/", vendor_order_items, name="vendor-order-items"),
    path("order_items/", get_order_items, name="order_items"), #Customer
    path('active_orders/', get_user_active_orders_json, name="get_active_orders_json"),  #customer
    path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),  # customer
    path('delete_order/<int:order_id>/', delete_order, name='delete_order'),  # customer
    path('delete_order_item/<int:item_id>/', delete_order_item, name='delete_order_item'),  # customer
    path('update_order_item_quantity/<int:item_id>/', update_order_item_quantity, name='update_order_item_quantity'),  # customer
]