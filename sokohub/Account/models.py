from django.db import models

# Account (id, names, email, phone ,passsword, role[vendor,customer])

class Account(models.Model):

    ROLE_CHOICES = (
        ('vendor', 'Vendor'),
        ('customer', 'Customer')
    )

    user_id = models.IntegerField(max_length=10, primary_key=True)
    names = models.CharField(max_length=25, null=False)
    email = models.CharField(unique=True, null=True, max_length=20)
    phone = models.CharField(unique=True, null=True)
    password = models.CharField(max_length=35, null=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

