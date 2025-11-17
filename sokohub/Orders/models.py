from django.db import models
from Account.models import Account
from Product.models import Product
import random

def generate_random_code():
    return random.randint(111111, 999999)

# Create your models here.
class Order(models.Model):

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled')
    ]

    order_id = models.IntegerField(primary_key=True, null=False, default=generate_random_code)
    total = models.IntegerField(default=0)
    status = models.CharField(choices=STATUS_CHOICES, default="pending")
    delivery_address = models.CharField()
    phone = models.CharField()
    created_at = models.DateField(auto_now_add=True)
    customer_id = models.ForeignKey(Account, to_field='user_id', null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.phone


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, to_field='order_id', null=True, on_delete=models.SET_NULL)
    product_id = models.ForeignKey(Product, to_field='product_id', null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField()
