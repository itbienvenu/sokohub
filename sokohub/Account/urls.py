from django.urls import path
from .views import accounts_list


urlpatterns = [
    path('', accounts_list, name='account-list')
]