from django.contrib import admin
from .models import Order,Cart

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_id', 'payment_id', 'delivery_status', 'ordered')
    list_filter = ('ordered', 'created')
    search_fields = ('user__username', 'payment_id', 'order_id')
    readonly_fields = ('created', 'payment_id', 'order_id')  # Make fields read-only if needed

admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
