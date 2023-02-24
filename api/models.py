from django.db import models
from django.contrib.auth.models import User
def product_directory_path(instance,filename):
    return 'products/{0}'.format(filename)

def category_directory_path(instance,filename):
    return 'category/{0}'.format(filename)

ORDER_STATUS = [
        ('pendiente', 'Pendiente'),
        ('en_camino', 'En camino'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to=category_directory_path)

    def __str__(self):
        return self.name

 
class Product(models.Model):
    user = models.ManyToManyField(User, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True, blank=True)
    franchise = models.CharField(max_length=200,null=False, blank=False)
    rating = models.FloatField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    recently_added = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    image =  models.ImageField(upload_to=product_directory_path)
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200,choices=ORDER_STATUS, default='pendiente')
    delivery_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    shippingPrice = models.FloatField(default=0.00)
    totalPrice = models.FloatField()

    def __str__(self):
        return self.created_at

class OrderItem(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True) 
    qty = models.IntegerField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.id


class Reviews(models.Model):
    rating = models.FloatField()
    review = models.CharField(max_length=250)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id


 




