from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import customer_required, vendor_required
from products.models import Product
from .models import Order, OrderItem
from .forms import OrderForm

@customer_required
def checkout(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.GET.get('quantity', 1))
    
    if quantity > product.stock:
        # Handle error
        return redirect('product_detail', pk=pk)

    total_price = product.price * quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.total = total_price
            order.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            product.stock -= quantity
            product.save()

            return redirect('order_confirmation', pk=order.pk)
    else:
        initial_data = {
            'phone': request.user.phone,
            'delivery_address': request.user.location
        }
        form = OrderForm(initial=initial_data)

    context = {
        'product': product,
        'quantity': quantity,
        'total_price': total_price,
        'form': form
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk)
    # Ensure user can only see their own orders
    if request.user != order.customer:
        return redirect('home')
    return render(request, 'orders/order_confirmation.html', {'order': order})

@customer_required
def customer_order_list(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'orders/customer_order_list.html', {'orders': orders})

@vendor_required
def vendor_order_list(request):
    # Get all order items for products belonging to this vendor
    order_items = OrderItem.objects.filter(product__vendor=request.user).order_by('-order__created_at')
    return render(request, 'orders/vendor_order_list.html', {'order_items': order_items})
