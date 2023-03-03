from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Category, Franchise
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
        fields = ('id', 'username', 'email', 'password')


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