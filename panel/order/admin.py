from django.contrib import admin
from order.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'status', 'user', 'expiration', 'month', 'create_at', 'updated_at')
    list_filter = ("user", "expiration", "status", "create_at", "updated_at", "month")
    search_fields = ['order_code', 'user']
admin.site.register(Order, OrderAdmin)