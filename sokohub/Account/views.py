from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account
from uuid import uuid4
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser

import random
# Create your views here.

def accounts_list(request):

    # [id(created automaticaly from uuidv4),names, email, password, phone, role]

    if request.method == "POST":

        names = request.POST.get('user_name')
        email = request.POST.get('user_email')
        phone = request.POST.get('user_phone_number')
        password = request.POST.get('user_password')
        role = request.POST.get('user_role')

        if not names or not email or not phone or not password or not role:
            messages.error(request, "All Fields are required")
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('account_create')
        
        new_account = Account(
            user_id=random.randint(111111,999999), 
            names=names,
            email=email, 
            phone=phone, 
            password=make_password(password), 
            user_type=role
            )
        new_account.save()


        context = {
            'message':"Account created well"
        }

        messages.success(request, context['message'])
        return redirect('user-login')



    all_accounts = Account.objects.all().order_by('names')

    context = {
        'accounts': all_accounts
    }

    return render(request, 'account/registration.html', context)


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("user_email")
        password = request.POST.get("user_password")

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            redirect_url = 'customer-dashboard' if user.user_type == 'customer' else 'vendor-dashboard'
            return redirect(redirect_url)

        raise ValueError("Invalid email or password")

    return render(request, 'account/login.html')


def vendor_dashboard(request):
    return render(request, 'account/vendor/vendor_page.html')

def customer_dashboard(request):
    return render(request, 'account/customer/customer_page.html')
