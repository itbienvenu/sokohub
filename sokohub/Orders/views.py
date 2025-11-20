from django.shortcuts import render,redirect
from .models import Order, OrderItem
from Product.models import Product
from django.contrib.auth.decorators import login_required
import random
from django.contrib import messages

from django.contrib import messages
# Create your views here.

@login_required
def create_order(request):
    user = request.user
    if request.method == "POST":
        try:
            if user.user_type != 'customer':
                messages.error(request, "Invalid user type")
                return redirect('all_products')
            
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
    if user.user_type != 'customer':
        messages.error(request, "Only customers are one to access Orders section")
        return redirect('all_products')
    


@login_required
def list_my_orders(request):
    user = request.user
    
    my_all_orders = Order.objects.filter(customer_id=user.pk).prefetch_related(
        'orderitem_set',
        'orderitem_set__product_id'
    ) 
    
    context = {
        "orders": my_all_orders
    }
    return render(request, 'orders/customer/my_orders.html', context)

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


@login_required
def vendor_order_items(request):
    vendor = request.user

    # 1. Authorization check
    if not vendor.user_type == 'vendor':
        return redirect('all_products') 

    vendor_order_items = OrderItem.objects.filter(
        product_id__user=vendor 
    ).select_related('order_id', 'product_id')

    context = {
        "order_items": vendor_order_items
    }

    return render(request, 'orders/vendor_order_items.html', context)


# customr get order items

@login_required
def get_order_items(request):
    order_id = request.GET.get('order_id')

    if not order_id:

        messages.error(request, "Invalid Ordere id")
        return redirect('')

    select_items = OrderItem.objects.filter(
        order_id=order_id,
        order_id__customer_id=request.user 
    ).select_related('product_id')

    context = {
        'select_items': select_items,
        'order_id': order_id
    }

    return render(request, 'orders/customer/order_items.html', context)