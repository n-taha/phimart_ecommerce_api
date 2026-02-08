from django.urls import path ,include
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet , CategoryViewSet, ProductImageViewSet, ReviewViewSet
from rest_framework_nested import routers
from order.views import CartViewSet, CartItemViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet)
router.register('orders', OrderViewSet, basename='orders')
product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-review')
product_router.register('images', ProductImageViewSet, basename='product-image')
router.register('carts', CartViewSet, basename='carts')
cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-item')
# urlpatterns = router.urls


urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path("", include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt'))
    # if we need to add more url endpoints...we can add
    # path('products/', include('product.product_urls')),
    # path("categories/", include('product.category_urls'))
]
