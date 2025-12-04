from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import vendor_required
from .models import Product
from .forms import ProductForm
from orders.models import OrderItem

def home(request):
    products = Product.objects.filter(status='active').order_by('-created_at')[:8]
    return render(request, 'products/home.html', {'products': products})

def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.filter(status='active')
    
    if query:
        products = products.filter(name__icontains=query)
        
    products = products.order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products, 'query': query})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@vendor_required
def vendor_dashboard(request):
    products = Product.objects.filter(vendor=request.user)
    active_products = products.filter(status='active').count()
    out_of_stock = products.filter(stock=0).count()
    pending_orders = OrderItem.objects.filter(product__vendor=request.user, order__status='pending').count()
    recent_products = products.order_by('-created_at')[:5]
    
    context = {
        'total_products': products.count(),
        'active_products': active_products,
        'out_of_stock': out_of_stock,
        'pending_orders': pending_orders,
        'recent_products': recent_products,
    }
    return render(request, 'products/vendor_dashboard.html', context)

@vendor_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save()
            return redirect('vendor_product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Add New Product'})

@vendor_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('vendor_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Edit Product', 'product': product})

@vendor_required
def vendor_product_list(request):
    products = Product.objects.filter(vendor=request.user).order_by('-created_at')
    return render(request, 'products/vendor_product_list.html', {'products': products})
