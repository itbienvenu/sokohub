from django.shortcuts import render
from .models import Product
from uuid import uuid4
# Create your views here.

def list_product(request):
    # [product_id, user_id, name, description, image, stock, quantity, price, status]

    if request.method == 'POST':
        name = request.POST.get('product_name')
        description = request.POST.get('product_description')
        image = request.POST.get('product_image')
        stock = request.POST.get('product_stock')
        price = request.POST.get('product_price')     
        quantity = request.POST.get('product_quantity')
     
        # status = request.POST.get('product_status')

        new_product = Product(
            product_id=str(uuid4()), 
            user_id=request.user, 
            name=name, 
            description=description, 
            image=image, 
            stock=stock, 
            price=price, 
            quantity=quantity
            )
        
        new_product.save




    products = Product.objects.all()

    

    context = {
        'product': products
    }

    return render(request, 'products/index.html',context)
