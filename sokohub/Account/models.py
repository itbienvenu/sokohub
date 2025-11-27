from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class AccountManager(BaseUserManager):
    def create_user(self, email, names, user_type="customer", password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, names=names, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, names, password=None, **extra_fields):
        user = self.create_user(
            email=email,
            names=names,
            user_type="vendor",
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ("vendor", "Vendor"),
        ("customer", "Customer"),
    ]

    user_id = models.BigAutoField(primary_key=True)
    names = models.CharField(max_length=50)
    
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
