from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Category, Franchise, Order, Category
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',"city","address","postal_code","country")


class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        fields = ["name"]

class ProductSerializer(serializers.ModelSerializer):
    franchise = FranchiseSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'rating', 'price', 'recently_added', 'best_seller', 'best_seller_image', 'image', 'favorite', 'franchise']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= ["delivery_date", "shippingPrice", "status", "totalPrice"]


class FranchiseSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source='product_set')
    franchise = serializers.CharField(source='name')
    class Meta:
        model = Franchise
        fields = ('franchise','products')