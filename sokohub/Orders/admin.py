from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	# Show the requested columns in the admin list view
	list_display = ('customer_id', 'total', 'status', 'created_at')
	list_filter = ('status', 'created_at')
	inlines = [OrderItemInline]