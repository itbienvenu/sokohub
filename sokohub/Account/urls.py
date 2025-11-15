from django.urls import path
from .views import accounts_list, user_login


urlpatterns = [
    path('', accounts_list, name='account-list'),
    path('login/',user_login, name='user-login' )
]