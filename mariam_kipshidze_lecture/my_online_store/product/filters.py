from django.db.models import Q
from django_filters import filters
from django_filters.rest_framework import FilterSet

from product.models import Product


class ProductFilter(FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    price_gte = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = filters.NumberFilter(field_name='price', lookup_expr='lte')
    search_field = filters.CharFilter(method='filter_search_field')

    def filter_search_field(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))

    class Meta:
        model = Product
        fields = ['title', 'description', 'price_gte', 'price_lte', 'search_field']
