from django.contrib import admin
from .models import Pizza, Drink, Order, OrderItem, Sauce

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'image')
    list_filter = ('price',)
    search_fields = ('name', 'description')

@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'image', 'image_url')
    list_filter = ('price',)
    search_fields = ('name',)

@admin.register(Sauce)
class SauceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'image', 'image_url')
    list_filter = ('price',)
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'pizza', 'drink', 'quantity')
    list_filter = ('pizza', 'drink')
    search_fields = ('pizza__name', 'drink__name')