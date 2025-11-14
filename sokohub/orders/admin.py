from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('get_subtotal',)
    fields = ('product', 'quantity', 'price', 'get_subtotal')

    def get_subtotal(self, obj):
        return f"${obj.get_subtotal()}"
    get_subtotal.short_description = 'Subtotal'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total', 'status', 'created_at', 'get_items_count')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username', 'customer__email', 'delivery_address')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
    list_per_page = 20

    def get_items_count(self, obj):
        return obj.get_items_count()
    get_items_count.short_description = 'Items Count'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'get_subtotal')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('get_subtotal',)

    def get_subtotal(self, obj):
        return f"${obj.get_subtotal()}"
    get_subtotal.short_description = 'Subtotal'