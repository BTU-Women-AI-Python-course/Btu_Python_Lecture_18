from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from product.models import Product
from product.pagination import SmallPageNumberPagination, ProductLimitOffsetPagination, ProductCursorPagination
from product.serializers import ProductSerializer, MutateProductSerializer, CreateProductSerializer, \
    ProductDynamicFieldsSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return ProductDynamicFieldsSerializer(*args, **kwargs, fields=['id', 'title'])
        elif self.action == 'retrieve':
            return ProductDynamicFieldsSerializer(
                *args, **kwargs, fields=['id', 'title', 'categories', 'price', 'tag'])
        elif self.action == 'create':
            return CreateProductSerializer(*args, **kwargs)
        return MutateProductSerializer(*args, **kwargs)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class ProductCreateListDetailViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = SmallPageNumberPagination
