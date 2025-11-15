from django.urls import path
from .views import accounts_list, user_login, vendor_dashboard, customer_dashboard



urlpatterns = [
    path('', accounts_list, name='account-list'),
    path('login/', user_login, name='user-login' ),
    path('vendor-dashboard/', vendor_dashboard, name='vendor-dashboard'),
    path('customer-dashboard/', customer_dashboard, name='customer-dashboard'),

]