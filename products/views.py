from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import vendor_required
from .models import Product, VendorCategory
from django.db.models import Count, Avg
from .forms import ProductForm, ProductImageFormSet, CategoryForm, ReviewForm
from orders.models import OrderItem

def home(request):
    products = Product.objects.filter(status='active').annotate(avg_rating=Avg('reviews__rating')).order_by('-created_at').prefetch_related('additional_images')[:8]
    return render(request, 'products/home.html', {'products': products})

def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    products = Product.objects.filter(status='active').annotate(avg_rating=Avg('reviews__rating'))
    
    if query:
        products = products.filter(name__icontains=query)
    
    if category_id:
        products = products.filter(category_id=category_id)
        
    products = products.order_by('-created_at')
    categories = VendorCategory.objects.annotate(product_count=Count('products')).all()
    
    return render(request, 'products/product_list.html', {
        'products': products, 
        'query': query,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Handle Review Submission
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('product_detail', pk=pk)
    else:
        review_form = ReviewForm()

    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'avg_rating': avg_rating,
        'review_count': reviews.count(),
    }
    return render(request, 'products/product_detail.html', context)

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
        form = ProductForm(request.POST, request.FILES, user=request.user)
        formset = ProductImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save()
            
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()
            formset.save_m2m() # Although no m2m here, good practice
            
            return redirect('vendor_product_list')
    else:
        form = ProductForm(user=request.user)
        formset = ProductImageFormSet()
    return render(request, 'products/product_form.html', {
        'form': form, 
        'formset': formset,
        'title': 'Add New Product'
    })

@vendor_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, user=request.user)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('vendor_product_list')
    else:
        form = ProductForm(instance=product, user=request.user)
        formset = ProductImageFormSet(instance=product)
    return render(request, 'products/product_form.html', {
        'form': form, 
        'formset': formset,
        'title': 'Edit Product', 
        'product': product
    })

@vendor_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('vendor_product_list')


@vendor_required
def vendor_product_list(request):
    products = Product.objects.filter(vendor=request.user).order_by('-created_at')
    return render(request, 'products/vendor_product_list.html', {'products': products})

@vendor_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = request.user
            category.save()
            return redirect('vendor_category_list')
    else:
        form = CategoryForm()
    return render(request, 'products/category_form.html', {'form': form})

@vendor_required
def edit_category(request, pk):
    category = get_object_or_404(VendorCategory, pk=pk, vendor=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('vendor_category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/category_form.html', {'form': form, 'title': 'Edit Category'})

@vendor_required
def vendor_category_list(request):
    categories = VendorCategory.objects.filter(vendor=request.user).order_by('-created_at')
    return render(request, 'products/vendor_category_list.html', {'categories': categories})


@vendor_required
def delete_category(request, pk):
    category = get_object_or_404(VendorCategory, pk=pk, vendor=request.user)
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('vendor_category_list')
