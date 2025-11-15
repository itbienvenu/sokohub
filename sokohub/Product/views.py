from django.shortcuts import render
from .models import Product

# Create your views here.

def list_product(request):
    products = Product.objects.all()
    context = {
        'product': products
    }

    return render(request, 'products/index.html',context)
