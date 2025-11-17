from django.shortcuts import render,redirect
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
import random

from django.contrib import messages
# Create your views here.
@login_required
def create_order(request):

    if request.method == "POST":
        user = request.user
        try:
            if user.user_type != 'customer':
                messages.error(request, "Invalid user type")
                return redirect('create_order')
            
            total = request.POST.get("order_total")
            delivery_address = request.POST.get("order_delivery_address")
            phone = request.POST.get("order_phone")
            customer_id = request.user

            create_order = Order (
                total = 0,
                delivery_address = "delivery_address",
                phone = "phone",
                customer_id = request.user
            )

            create_order.save()
        except Exception as e:
            raise ValueError("Error creating order", e, "Reques user: ", request.user.user_id)   
    return render(request, 'orders/index.html')


@login_required
def add_product_to_order(request):
    if request.method == "POST":
        try:
            order_id = request.POST.get('order_id')
            product_id = request.POST.get('product_id')
            quantity = request.POST.get('product_quantity')

            create_order_item = OrderItem(
                order_id = order_id,
                product_id = product_id,
                quantity = quantity
            )

            create_order_item.save()
        except Exception as e:
            raise ValueError("Error creating the order itme", e)
