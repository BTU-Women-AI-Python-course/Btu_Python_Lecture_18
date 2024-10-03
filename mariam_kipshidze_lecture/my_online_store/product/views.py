from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from product.filters import ProductFilter
from product.models import Product
from product.pagination import SmallPageNumberPagination, ProductLimitOffsetPagination, ProductCursorPagination
from product.serializers import ProductSerializer, MutateProductSerializer, CreateProductSerializer, \
    ProductDynamicFieldsSerializer
from user.permissiopns import IsActiveUser


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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    permission_classes = [IsAuthenticated, IsActiveUser]

    @action(detail=False, methods=['get', 'post'])
    def latest_products(self, request, *args, **kwargs):
        """
        This action retrieves a list of the latest products added.
        Accessed via /products/latest_products/
        """
        latest_products = self.get_queryset().order_by('-create')[:3]
        serializer = self.get_serializer(latest_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated],
            serializer_class=MutateProductSerializer)
    def product_data(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)
