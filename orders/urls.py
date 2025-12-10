from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:pk>/', views.checkout, name='checkout'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_cart, name='checkout_cart'),
    path('order/confirmation/<int:pk>/', views.order_confirmation, name='order_confirmation'),
    path('order/update/<int:pk>/', views.update_order, name='update_order'),
    path('my-orders/', views.customer_order_list, name='customer_order_list'),
    path('vendor/orders/', views.vendor_order_list, name='vendor_order_list'),
    path('vendor/orders/complete/<int:pk>/', views.mark_order_completed, name='mark_order_completed'),
]
