from django.shortcuts import render,redirect
from .models import Order, OrderItem
from Product.models import Product
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
                delivery_address = delivery_address,
                phone = phone,
                customer_id = request.user
            )

            create_order.save()
        except Exception as e:
            raise ValueError("Error creating order", e, "Reques user: ", request.user.user_id)   
    return render(request, 'orders/index.html')



def list_my_orders(request):
    user = request.user
    
    # Filter using the Foreign Key ID field (e.g., 'customer_id') and pass the PK
    my_all_orders = Order.objects.filter(customer_id=user.pk) 
    
    context = {
        "orders": my_all_orders
    }
    return render(request, 'orders/my_orders.html', context)


@login_required
def add_product_to_order(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('product_quantity')

        if not order_id:
            raise ValueError("order_id was not provided in the POST request")

        order = Order.objects.get(pk=order_id)
        product = Product.objects.get(pk=product_id)

        OrderItem.objects.create(
            order_id=order,
            product_id=product,
            quantity=quantity
        )
        context = {
            "message":"Product is created"
        }
        return redirect("all_products")


def list_order_items(request):
    pass