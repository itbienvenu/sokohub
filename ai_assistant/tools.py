from products.models import Product, VendorCategory
from orders.models import Cart, CartItem, Order, OrderItem
from django.db.models import Sum, Count, Q
from django.core.exceptions import ObjectDoesNotExist

def search_products(query=None, min_price=None, max_price=None, category_name=None):
    """
    Search for products based on keywords, price range, and category.
    """
    products = Product.objects.filter(status='active')

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    if min_price is not None:
        products = products.filter(price__gte=min_price)
    
    if max_price is not None:
        products = products.filter(price__lte=max_price)
        
    if category_name:
        products = products.filter(category__name__icontains=category_name)

    results = []
    for p in products[:10]: # Limit to 10 results
        results.append({
            "id": p.id,
            "name": p.name,
            "price": float(p.price),
            "stock": p.stock,
            "vendor": p.vendor.username
        })
    return results

def add_to_cart(user, product_id, quantity=1):
    """
    Add a product to the user's cart.
    """
    if not user.is_authenticated:
        return {"error": "User must be logged in to add to cart."}
    
    try:
        product = Product.objects.get(id=product_id, status='active')
    except ObjectDoesNotExist:
        return {"error": f"Product with ID {product_id} not found."}
        
    if product.stock < quantity:
        return {"error": f"Insufficient stock. Only {product.stock} available."}

    cart, created = Cart.objects.get_or_create(customer=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    
    cart_item.save()
    return {"success": True, "message": f"Added {quantity} x {product.name} to cart."}

def get_vendor_stats(user):
    """
    Get sales and inventory statistics for a vendor.
    """
    if not user.is_authenticated or user.user_type != 'vendor':
        return {"error": "User is not authorized as a vendor."}

    total_products = Product.objects.filter(vendor=user).count()
    active_products = Product.objects.filter(vendor=user, status='active').count()
    
    sold_items = OrderItem.objects.filter(
        product__vendor=user, 
        order__status='completed'
    )
    
    total_revenue = sold_items.aggregate(total=Sum('price'))['total'] or 0.0
    total_sales_count = sold_items.count()
    
    return {
        "store_name": user.username,
        "total_products": total_products,
        "active_products": active_products,
        "total_revenue": float(total_revenue),
        "total_sales": total_sales_count
    }
