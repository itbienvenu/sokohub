from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'user', 'price', 'stock')
	list_filter = ('user', 'status')
	search_fields = ('name', 'description')