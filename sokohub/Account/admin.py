
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Account.models import Account

class AccountAdmin(UserAdmin):
    model = Account

    list_display = ("email", "names", "user_type", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "user_type")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("names", "phone", "user_type")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "names", "user_type", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(Account, AccountAdmin)
