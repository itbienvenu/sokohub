from django.urls import path
from . import views

urlpatterns = [
    # Customer order routes
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.customer_orders, name='customer_orders'),
    path('my-orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # Vendor order routes
    path('vendor/orders/', views.vendor_orders, name='vendor_orders'),

    # API routes
    path('api/check-stock/<int:product_id>/', views.check_stock, name='check_stock'),
]
