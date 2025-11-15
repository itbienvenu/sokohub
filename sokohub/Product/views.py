from django.shortcuts import render, redirect
from .models import Product
from Account.models import Account

from uuid import uuid4
# Create your views here.
user_id="afe9586f-2224-444b-a725-8148f49ef1df"
def create_product(request):
    # [product_id, user_id, name, description, image, stock, quantity, price, status]
    
    vendor = Account.objects.get(pk=user_id)
    if request.method == 'POST' and request.user.is_authenticated:
        vendor_id = request.user.pk
        name = request.POST.get('product_name')
        description = request.POST.get('product_description')
        image = request.POST.get('product_image')
        stock = request.POST.get('product_stock')
        price = request.POST.get('product_price')     
        quantity = request.POST.get('product_quantity')

        print("name:", name)
        print("description  :", description)
        print("image  :", image)
        print("stock  :", stock)
        print("price  :", price)
        print("quantity  :", quantity)
     
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
