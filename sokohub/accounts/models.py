from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


# firstname, lastname ,email, password, ......., isAdmin, isActive, ....

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
    )

    # user_permissions = models.ManyToManyField(Permission, blank=True)
    # user_groups = models.ManyToManyField(Group, blank=True)

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"
