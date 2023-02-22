from django.contrib import admin
from .models import Product, Order, OrderItem, Category, Reviews


# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Reviews)
