from django.contrib import admin
from .models import Order
from restaurantmgmt.models import RestaurantManagement

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'restaurant', 'food_item', 'quantity', 'total_price', 'order_date')
    list_filter = ('restaurant', 'order_date')
    search_fields = ('name', 'restaurant', 'food_item')

@admin.register(RestaurantManagement)
class RestaurantManagementAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'get_rating_display', 'created_by')
    list_filter = ('rating', 'created_at')
    search_fields = ('restaurant__name', 'description')
