from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from Account.models import Account
from django.contrib.auth.decorators import login_required
from uuid import uuid4
from django.contrib import messages
from Account.security import vendor_required, customer_required
# Create your views here.


@login_required
@vendor_required
def create_product(request):
    user = request.user
    # vendor = Account.objects.get(pk=user.user_id)
    if request.method == 'POST':
        vendor_id = user
        name = request.POST.get('product_name')
        description = request.POST.get('product_description')
        image = request.POST.get('product_image')
        stock = request.POST.get('product_stock')
        price = request.POST.get('product_price')     
        # status = request.POST.get('product_status')

        new_product = Product(
            product_id=str(uuid4()), 
            user=vendor_id,
            name=name, 
            description=description, 
            image=image, 
            stock=stock, 
            price=price, 
            )
        
        new_product.save()
        messages.success(request, "Product created well")
        return redirect('vendor-dashboard')
    

def get_all_products(request):
    products = Product.objects.all().select_related('user')
    
    context = {
        "products": products
    }
    return render(request, 'products/customer/products.html', context)


@login_required
@vendor_required
def get_my_products(request):
    vendor = request.user
    # go in databse and fetch prodcts for loged in vendor

    vendor_products = Product.objects.filter(user=vendor)
    context = {
        "products":vendor_products
    }

    return render(request, 'products/vendor/my_products.html', context)

def vendor_add_products(request):
    return render(request, 'account/vendor/vendor_add_products.html')

@login_required
@vendor_required
def edit_product(request):
    if request.method == "GET":
        product_id = request.GET.get('product_id')

        try:
            product = get_object_or_404(
                Product, 
                pk=product_id, 
                user=request.user
            )
        except:
            messages.error(request, "Product not found or you do not have permission to edit it.")
            return redirect("vendor_products")
        
        context = {
            "product": product
        }
        return render(request, 'products/vendor/edit_product.html', context)
    
    elif request.method == "POST":

        p_id = request.POST.get('product_id')
        
        try:
            product = Product.objects.get(pk=p_id, user=request.user)
        except Product.DoesNotExist:
            messages.error(request, "Product not found or unauthorized update attempted.")
            return redirect("vendor_products")


        product.name = request.POST.get('product_name')
        product.description = request.POST.get('product_description')
        product.image = request.POST.get('product_image')

        try:
            product.stock = int(request.POST.get('product_stock'))
            product.price = float(request.POST.get('product_price'))
        except (ValueError, TypeError):
            messages.error(request, "Stock, Price, and Quantity must be valid numbers.")
            return redirect('edit_product', product_id=p_id)
        product.save()

        messages.success(request, f"Product '{product.name}' updated successfully!")
        return redirect("vendor_products")
    
    return redirect("vendor_products")


@login_required
@vendor_required
def delete_product(request):

    product_id = request.POST.get('product_id') or request.GET.get('product_id')
    
    if not product_id:
        messages.error(request, "Product ID is missing.")
        return redirect("vendor_products") 
    try:

        product = get_object_or_404(
            Product, 
            pk=product_id, 
            user=request.user 
        )
    except Exception:
        messages.error(request, "Product not found or unauthorized deletion attempted.")
        return redirect("vendor_products")

    if request.method == "POST":
        product_name = product.name

        product.delete() 

        messages.success(request, f"Product '{product_name}' has been successfully deleted.")
        return redirect("vendor_products")
    messages.warning(request, "Deletion requires confirmation.")
    return redirect("vendor_products")



def product_details(request):
    product_id = request.GET.get('product_id')

    product = get_object_or_404(
        Product, 
        pk=product_id
    )
    
    vendor_name = product.user.names 
    
    context = {
        "product": product,
        "vendor_name": vendor_name, 
    }
    
    return render(request, 'products/customer/product_details.html', context)

def landing_page(request):
    return render(request, 'landing_page.html')