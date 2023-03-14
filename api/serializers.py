from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Category, Franchise, Order, Category, Reviews
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

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class FranchiseSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Franchise
        fields = ["name","category"]

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    

    class Meta:
        model = Reviews
        fields = ('id', 'rating', 'review', 'date_created', 'user',)
        read_only_fields = ("id", "date_created","user")

    def get_user(self, obj):
        return obj.user.username

class ProductSerializer(serializers.ModelSerializer):
    franchise = FranchiseSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'rating', 'price', 'recently_added', 'best_seller', 'best_seller_image', 'image', 'franchise']

class ProductDetailSerializer(serializers.ModelSerializer):
    franchise = FranchiseSerializer(read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["favorite_by",]

    def get_reviews(self, obj):
        reviews = Reviews.objects.filter(product=obj).order_by('-date_created')
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


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



  