from django.db import models
from Account.models import Account

# Create your models here.
class Product(models.Model):
    product_id = models.CharField(primary_key=True)
    user = models.ForeignKey(Account, to_field='user_id', on_delete = models.CASCADE)
    image = models.CharField()
    status = models.CharField(default='active')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
