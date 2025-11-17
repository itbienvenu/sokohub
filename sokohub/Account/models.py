from django.db import models

# Account (id, names, email, phone ,passsword, role[vendor,customer], created_at)

class Account(models.Model):

    ROLE_CHOICES = [
        ('vendor', 'Vendor'),
        ('customer', 'Customer')
    ]

    user_id = models.BigIntegerField(primary_key=True)
    names = models.CharField(max_length=25, null=False)
    email = models.CharField(unique=True, null=True, max_length=20)
    phone = models.CharField(unique=True, null=True)
    password = models.CharField(max_length=35, null=False)
    user_type = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateField(auto_now_add=True)
    last_login = models.DateField(blank=True, null=True)
    is_authenticated = models.BooleanField(default=True)

    def __str__(self):
        return self.email

