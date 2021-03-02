from django.contrib import admin
from .models import Product, Category, Customer, ShippingAddress, Order, OrderItem, Coupon, Rating

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(Rating)

