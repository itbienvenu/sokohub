from django.shortcuts import render, redirect
from .models import Account
from uuid import uuid4
from django.contrib.auth import authenticate, login

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
            raise ValueError("Missing data")
        
        new_account = Account(
            user_id=uuid4(), 
            names=names, 
            email=email, 
            phone=phone, 
            password=password, 
            user_type=role
            )
        new_account.save()

        context = {
            'message':"Account created well"
        }

        return render(request, 'account/login.html', context)



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
        if user is not None:
            return render(request, 'account/home.html', context="")
        else:
            return render(request, 'account/login.html', {"error":"Invalid email or password"})
