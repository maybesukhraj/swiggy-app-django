from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'restaurant', 'food_item', 'quantity', 'total_price', 'order_date')
    list_filter = ('restaurant', 'order_date')
    search_fields = ('name', 'restaurant', 'food_item')
