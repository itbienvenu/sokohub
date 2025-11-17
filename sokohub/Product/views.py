from django.shortcuts import render, redirect
from .models import Product
from Account.models import Account
from django.contrib.auth.decorators import login_required
from uuid import uuid4
# Create your views here.


@login_required
def create_product(request):
    # [product_id, user_id, name, description, image, stock, quantity, price, status]
    user = request.user
    # vendor = Account.objects.get(pk=user.user_id)
    if request.method == 'POST':
        vendor_id = user
        name = request.POST.get('product_name')
        description = request.POST.get('product_description')
        image = request.POST.get('product_image')
        stock = request.POST.get('product_stock')
        price = request.POST.get('product_price')     
        quantity = request.POST.get('product_quantity')     
        # status = request.POST.get('product_status')

        new_product = Product(
            product_id=str(uuid4()), 
            user=vendor_id,
            name=name, 
            description=description, 
            image=image, 
            stock=stock, 
            price=price, 
            quantity=quantity
            )
        
        new_product.save()
        return redirect('vendor-dashboard')



def get_my_products(request):
    vendor = request.user
    # go in databse and fetch prodcts for loged in vendor

    vendor_products = Product.objects.filter(user=vendor)

    context = {
        "products":vendor_products
    }

    return render(request, 'products/products.html', context)

