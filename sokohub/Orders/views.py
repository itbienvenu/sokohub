from django.shortcuts import render,redirect
from .models import Order, OrderItem
from Product.models import Product
from django.contrib.auth.decorators import login_required
import random
from django.contrib import messages
from django.http import JsonResponse

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
            messages.success(request, "Order created successfully")
            return redirect('my_orders')

        except Exception as e:
            raise ValueError("Error creating order", e, "Reques user: ", request.user.user_id)  
    if user.user_type != 'customer':
        messages.error(request, "Only customers are one to access Orders section")
        return redirect('all_products')
    return redirect('my_orders')
    


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
        order.total += product.price * int(quantity)
        order.save()
        messages.success(request, f"Product is Added to order {order_id} successfully")
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

        messages.error(request, "Invalid Order id")
        return redirect('')

    select_items = OrderItem.objects.filter(
        order_id=order_id,
        order_id__customer_id=request.user 
    ).select_related('product_id')

    context = {
        'items': select_items,
        'order_id': order_id
    }

    return render(request, 'orders/customer/order_items.html', context)



@login_required
def get_user_active_orders_json(request):
    """
    Fetches the user's active orders (pending/processing) and returns them as JSON.
    """
    user = request.user
    
    active_orders = Order.objects.filter(
        customer_id=user.pk,
        status__in=['pending', 'processing'] 
    ).order_by('-created_at')
    print(user)
    order_list = []
    for order in active_orders:
        order_list.append({
            'order_id': order.order_id, 
            'display_name': f"Order #{order.order_id} ({order.status.capitalize()})",
            'created_at': order.created_at.strftime("%Y-%m-%d"),
            'status': order.status,
        })

    return JsonResponse({'orders': order_list})


@login_required
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id, customer_id=request.user)
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            messages.success(request, "Order cancelled successfully.")
        else:
            messages.error(request, "Only pending orders can be cancelled.")
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
    
    return redirect('my_orders')

@login_required
def delete_order(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id, customer_id=request.user)
        order.delete()
        messages.success(request, "Order deleted successfully.")
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
    
    return redirect('my_orders')

@login_required
def delete_order_item(request, item_id):
    try:
        order_item = OrderItem.objects.get(item_id=item_id, order_id__customer_id=request.user)
        order = order_item.order_id
        order.total -= order_item.product_id.price * order_item.quantity
        order.save()
        order_item.delete()
        messages.success(request, "Order item deleted successfully.")
    except OrderItem.DoesNotExist:
        messages.error(request, "Order item not found.")
    
    return redirect('my_orders')


@login_required
def update_order_item_quantity(request, item_id):
    if request.method == "POST":
        new_quantity = request.POST.get('new_quantity')
        try:
            order_item = OrderItem.objects.get(item_id=item_id, order_id__customer_id=request.user)
            order = order_item.order_id
            order.total -= order_item.product_id.price * order_item.quantity
            print("New Quantity:", new_quantity)
            order_item.quantity = int(new_quantity)
            order_item.save()
            order.total += order_item.product_id.price * order_item.quantity
            order.save()
            messages.success(request, "Order item quantity updated successfully.")
        except OrderItem.DoesNotExist:
            messages.error(request, "Order item not found.")
    
    return redirect('my_orders')
