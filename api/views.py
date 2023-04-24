from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ProductSerializer, CategorySerializer, OrderSerializer, \
     FranchiseSerializer, ReviewSerializer, ProductDetailSerializer, SearchProductSerializer, OrderItemSerializer
from django.contrib.auth import authenticate, login
from .models import Product, Category, Order, Franchise, Reviews, OrderItem
from django.db.models import Q

User = get_user_model()

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):        
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(user_id=request.user.id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FranchiseView(APIView):
    def get(self, request, category):
        franchise  = Franchise.objects.filter(category= category)
        serializer = FranchiseSerializer(franchise, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FavoriteProductView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        favorite_products = Product.objects.filter(favorite_by=user)
        serializer = ProductSerializer(favorite_products, many=True)
        return Response({'favorites': serializer.data})

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        product.favorite_by.add(user)
        product.save()
        return Response({'status': 'Product added to whishlist'}, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)
        product.favorite_by.remove(request.user)
        return Response({'status': 'Product removed from whishlist'})

class ReviewProductAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id,*args, **kwargs):
        if Reviews.objects.filter(product_id=product_id, user=request.user).exists():
            return Response({"message":"You already have been comment this product"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                product = get_object_or_404(Product, id=product_id)
                review = serializer.save(user=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        reviews = Reviews.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DetailProductView(APIView):
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchAPIView(generics.ListAPIView):
    serializer_class = SearchProductSerializer 
    queryset = Product.objects.all() 

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query is not None:
            # searching by product name/franchise/category
            products = self.queryset.filter(Q(name__icontains=query) | Q(franchise__name__icontains=query) | Q(franchise__category__name=query))
        return products 

class OrderItemListAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        user = self.request.user
        return OrderItem.objects.filter(user_id=user)

class OrderItemAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        qty = request.data.get('qty', 1)
        user = request.user

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=404)

        order_item, created = OrderItem.objects.get_or_create(
            user_id=user,
            product_id=product,
            order_id=None,
            defaults={'qty': qty},
        )
        serializer = OrderItemSerializer(order_item)

        return Response(serializer.data, status=201)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            order_item = OrderItem.objects.get(user_id=request.user, product_id=product)
        except OrderItem.DoesNotExist:
            return Response({'detail': 'Order item not found.'}, status=status.HTTP_404_NOT_FOUND)

        order_item.delete()

        return Response({'detail': 'Order item deleted.'}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            order_item = OrderItem.objects.get(user_id=request.user, product_id=product)
        except OrderItem.DoesNotExist:
            return Response({'detail': 'Order item not found.'}, status=status.HTTP_404_NOT_FOUND)

        qty = request.data.get('qty')
        if qty is None:
            return Response({'detail': 'Qty is required.'}, status=status.HTTP_400_BAD_REQUEST)

        order_item.qty = qty
        order_item.save()

        serializer = OrderItemSerializer(order_item)

        return Response(serializer.data)

