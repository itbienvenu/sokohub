from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:pk>/', views.checkout, name='checkout'),
    path('order/confirmation/<int:pk>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.customer_order_list, name='customer_order_list'),
    path('vendor/orders/', views.vendor_order_list, name='vendor_order_list'),
    path('vendor/orders/complete/<int:pk>/', views.mark_order_completed, name='mark_order_completed'),
]
