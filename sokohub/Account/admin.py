from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


@admin.register(Account)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('names', 'phone', 'user_type')}), # Combined custom fields
        (
            'Permissions', 
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    ordering = ('email',) 
    
    search_fields = ('email', 'names', 'phone')
    
    list_display = ('names', 'email', 'user_type', 'is_staff', 'is_active')
    
    list_filter = ('is_staff', 'is_active', 'user_type')
