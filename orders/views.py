from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import customer_required, vendor_required
from products.models import Product
from .models import Order, OrderItem, Cart, CartItem
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

@vendor_required
def mark_order_completed(request, pk):
    order = get_object_or_404(Order, pk=pk)
    # Check if the vendor owns the product in this order
    # Since checkout creates one order per product transaction, we can check the first item
    order_item = order.items.first()
    if order_item and order_item.product.vendor == request.user:
        order.status = 'completed'
        order.save()
    return redirect('vendor_order_list')

@customer_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, "Product quantity updated in cart.")
    else:
        messages.success(request, "Product added to cart.")
        
    return redirect('view_cart')

@customer_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    return render(request, 'orders/cart.html', {'cart': cart})

@customer_required
def update_cart_item(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('view_cart')

@customer_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')

@customer_required
def checkout_cart(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('product_list')

    total_price = cart.total_price

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.total = total_price
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                # Deduct stock
                item.product.stock -= item.quantity
                item.product.save()

            # Clear cart
            cart.items.all().delete()
            return redirect('order_confirmation', pk=order.pk)
    else:
        initial_data = {
            'phone': getattr(request.user, 'phone', ''),
            'delivery_address': getattr(request.user, 'location', '')
        }
        form = OrderForm(initial=initial_data)

    return render(request, 'orders/checkout_cart.html', {
        'cart': cart,
        'form': form,
        'total_price': total_price
    })

@customer_required
def update_order(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    
    if order.status != 'pending':
        messages.error(request, "You cannot update a completed order.")
        return redirect('customer_order_list')

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order updated successfully.")
            return redirect('order_confirmation', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    
    return render(request, 'orders/update_order.html', {'order': order, 'form': form})
