from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account
from Product.models import Product
from Orders.models import Order, OrderItem
from uuid import uuid4
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser
from .security import vendor_required, customer_required
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
            return redirect('account-create')
        
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
            redirect_url = 'all_products' if user.user_type == 'customer' else 'vendor-dashboard'
            return redirect(redirect_url)

        messages.error(request, "Invalid email or password.")
        return redirect('user-login')

    return render(request, 'account/login.html')

@vendor_required
def vendor_dashboard(request):
    vendor = request.user
    total_vendor_products = Product.objects.filter(user=vendor).count()
    activer_vendor_products = Product.objects.filter(user=vendor, status=True).count()
    out_of_stock_products = Product.objects.filter(user=vendor, stock=0).count()
    vendor_pending_orders = OrderItem.objects.filter(product_id__user=vendor, order_id__status='pending').count()
    # vendor_pending_orders = Order.objects.filter(vendor=vendor, status='pending').count()

    top_most_vendor_products = Product.objects.filter(user=vendor).order_by('-stock')[:5]

    context = {
        "total_vendor_products": total_vendor_products,
        "activer_vendor_products": activer_vendor_products,
        "out_of_stock_products": out_of_stock_products,
        "vendor_pending_orders": vendor_pending_orders,
        "top_most_vendor_products": top_most_vendor_products
    }

    return render(request, 'account/vendor/vendor_page.html', context)
    # return render(request, 'account/vendor/vendor_page.html')

@customer_required
def customer_dashboard(request):
    return render(request, 'account/customer/customer_page.html')

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('landing_page')



@vendor_required
def vendor_analytics(request):
    vendor = request.user
    total_vendor_products = Product.objects.filter(user=vendor).count()
    activer_vendor_products = Product.objects.filter(vendor=vendor, status=True).count()
    out_of_stock_products = Product.objects.filter(user=vendor, stock=0).count()
    vendor_pending_orders = Order.objects.filter(vendor=vendor, status='pending').count()
    top_most_vendor_products = Product.objects.filter(user=vendor).order_by('-stock')[:5]

    context = {
        "total_vendor_products": total_vendor_products,
        "activer_vendor_products": activer_vendor_products,
        "out_of_stock_products": out_of_stock_products,
        "vendor_pending_orders": vendor_pending_orders,
        "top_most_vendor_products": top_most_vendor_products
    }

    return render(request, 'account/vendor/vendor_dashboard.html', context)