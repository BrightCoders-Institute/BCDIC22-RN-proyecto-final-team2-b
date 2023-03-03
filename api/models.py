from django.db import models
from django.contrib.auth import models as auth_models

def product_directory_path(instance,filename):
    return 'products/{0}'.format(filename)

def category_directory_path(instance,filename):
    return 'category/{0}'.format(filename)

def bestseller_path(instance,filename):
    return 'bestseller/{0}'.format(filename)

ORDER_STATUS = [
        ('pendiente', 'Pendiente'),
        ('en_camino', 'En camino'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

class UserManager(auth_models.BaseUserManager):
    def create_user(self, username: str, email: str, password: str = None, is_staff=False, is_superuser=False) -> "User":
        user = self.model(email=self.normalize_email(email))
        user.username = username
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_superuser(self, username:str, email:str, password:str)->"User":
        user = self.create_user(
            username=username, 
            email=email,
            password=password, 
            is_staff=True,
            is_superuser=True,
          
        )
        user.save()

class CustomUser(auth_models.AbstractUser):
    username = models.CharField(verbose_name="Username",max_length=255)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "username"]

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to=category_directory_path)

    def __str__(self):
        return self.name

class Franchise(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
 
class Product(models.Model):
    user = models.ManyToManyField(CustomUser, blank=True)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True, blank=True)
    rating = models.FloatField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    recently_added = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    best_seller_image = models.ImageField(upload_to=product_directory_path, default="category/Marvel_Logo.svg.png")
    image =  models.ImageField(upload_to=bestseller_path)
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Order(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=200,choices=ORDER_STATUS, default='pendiente')
    delivery_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    shippingPrice = models.FloatField(default=0.00)
    totalPrice = models.FloatField()

    def __str__(self):
        return self.created_at

class OrderItem(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True) 
    qty = models.IntegerField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.id


class Reviews(models.Model):
    rating = models.FloatField()
    review = models.CharField(max_length=250)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id


 




