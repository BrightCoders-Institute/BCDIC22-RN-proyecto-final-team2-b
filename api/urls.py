from django.urls import path, include
from .views import SignUpView, LoginView, ProductViewSet, CategoryViewSet, UserView, OrderView, FranchiseView, FavoriteProductView, \
    ReviewProductAPIView, DetailProductView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('franchises/<int:category>/', FranchiseView.as_view(), name='franchises-by-category'),
    path('users/data/', UserView.as_view(), name='users-data'),
    path('users/orders/', OrderView.as_view(), name='users-orders'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),

    #favorite
    path('product/favorite/<int:product_id>/', FavoriteProductView.as_view(), name='favorite'),
    path('product/favorite/', FavoriteProductView.as_view(), name='favorite'),

    #reviews
    path('product/review/<int:product_id>/', ReviewProductAPIView.as_view(), name='review'),

    #get product
    path('product/detail/<int:product_id>/', DetailProductView.as_view(), name='review'),


   

]