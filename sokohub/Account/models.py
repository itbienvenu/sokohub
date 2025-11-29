from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager 

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class Account(AbstractUser):

    ROLE_CHOICES = [
        ("vendor", "Vendor"),
        ("customer", "Customer"),
    ]

    user_id = models.BigAutoField(primary_key=True)
    names = models.CharField(max_length=50)
    username = None
    email = models.EmailField(unique=True, max_length=60)
    phone = models.CharField(unique=True, null=True, max_length=20)

    user_type = models.CharField(max_length=10, choices=ROLE_CHOICES, default="customer")
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager() 

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["names"] 

    def __str__(self):
        return self.email