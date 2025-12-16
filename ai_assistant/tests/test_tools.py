from django.test import TestCase
from ai_assistant.tools import search_products, add_to_cart, get_vendor_stats
from products.models import Product, VendorCategory
from orders.models import Cart, CartItem, Order, OrderItem
from accounts.models import User
from django.utils import timezone

class ToolsTest(TestCase):
    def setUp(self):
        self.vendor = User.objects.create_user(username='vendor', password='password', email='vendor@example.com', user_type='vendor')
        self.customer = User.objects.create_user(username='customer', password='password', email='customer@example.com', user_type='customer')
        self.category = VendorCategory.objects.create(vendor=self.vendor, name="Electronics", description="Tech stuff")
        self.product = Product.objects.create(
            vendor=self.vendor, 
            category=self.category,
            name="Smartphone", 
            description="Black 128GB", 
            price=199.99, 
            stock=10,
            status='active'
        )

    def test_search_products(self):
        # Case 1: Exact Match
        results = search_products(query="Smartphone")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Smartphone")
        
        # Case 2: Price Filter
        results = search_products(max_price=200)
        self.assertEqual(len(results), 1)
        
        results = search_products(max_price=100)
        self.assertEqual(len(results), 0)
        
        # Case 3: Category
        results = search_products(category_name="Electro")
        self.assertEqual(len(results), 1)

    def test_add_to_cart(self):
        # Case 1: Success
        result = add_to_cart(self.customer, self.product.id, quantity=2)
        self.assertIn("success", result)
        
        cart = Cart.objects.get(customer=self.customer)
        item = CartItem.objects.get(cart=cart)
        self.assertEqual(item.quantity, 2)
        
        # Case 2: Insufficient Stock
        result = add_to_cart(self.customer, self.product.id, quantity=20)
        self.assertIn("error", result)

    def test_get_vendor_stats(self):
        # Create a completed order
        order = Order.objects.create(customer=self.customer, status='completed', total=199.99)
        OrderItem.objects.create(order=order, product=self.product, quantity=1, price=199.99)
        
        # Case 1: Valid Vendor
        stats = get_vendor_stats(self.vendor)
        self.assertEqual(stats['total_sales'], 1)
        self.assertEqual(stats['total_revenue'], 199.99)
        
        # Case 2: Not a vendor
        stats = get_vendor_stats(self.customer)
        self.assertIn("error", stats)
