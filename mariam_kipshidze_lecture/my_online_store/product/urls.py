from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from product.views import ProductViewSet, ProductCreateListDetailViewSet

router = SimpleRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'products_2', ProductCreateListDetailViewSet, basename='products_2')

urlpatterns = [
    path('', include(router.urls))
]
