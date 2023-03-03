from django.contrib import admin
from .models import Product, Order, OrderItem, Category, Reviews, Franchise, CustomUser


# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Reviews)
admin.site.register(Franchise)
admin.site.register(CustomUser)
