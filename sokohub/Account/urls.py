from django.urls import path
from .views import accounts_list, user_login, vendor_dashboard, customer_dashboard, user_logout



urlpatterns = [
    path('', accounts_list, name='account-create'),
    path('login/', user_login, name='user-login' ),
    path('vendor-dashboard/', vendor_dashboard, name='vendor-dashboard'),
    path('customer-dashboard/', customer_dashboard, name='customer-dashboard'),
    path('logout/', user_logout, name='user-logout'),

]