from django.contrib import admin

from .models import Cart, Order


class ProductInline(admin.TabularInline):
    model = Cart.products.through


class CartAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]


class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
