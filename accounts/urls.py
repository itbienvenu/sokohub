from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('password_reset_confirm/', views.reset_password, name='password_reset_confirm'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('set_new_password/<int:user_id>/<str:token>/', views.set_new_password, name='set_new_password'),

]
