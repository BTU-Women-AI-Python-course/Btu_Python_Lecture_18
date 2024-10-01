# Django Rest Framework Pagination

Django REST Framework (DRF) provides several ways to implement pagination in your API views, 
allowing you to limit the number of results returned in a single response. 
This helps improve performance and enhances user experience when dealing with large datasets.

### Pagination Types in Django REST Framework

1. **PageNumberPagination**:
   - This is the default pagination style in DRF. It provides pagination by splitting the results into pages and using query parameters to navigate between them.
   - **Usage**:
     ```python
     from rest_framework.pagination import PageNumberPagination

     class MyPageNumberPagination(PageNumberPagination):
         page_size = 10  # Default number of results per page
         page_size_query_param = 'page_size'  # Allow client to set page size
         max_page_size = 100  # Maximum limit for page size

     # In your view
     from rest_framework.views import APIView
     from rest_framework.response import Response

     class MyAPIView(APIView):
         pagination_class = MyPageNumberPagination

         def get(self, request):
             queryset = MyModel.objects.all()
             paginator = self.pagination_class()
             page = paginator.paginate_queryset(queryset, request)
             return paginator.get_paginated_response(page)
     ```

2. **LimitOffsetPagination**:
   - This style uses a `limit` and `offset` to control the number of results returned. It is useful for implementing infinite scrolling.
   - **Usage**:
     ```python
     from rest_framework.pagination import LimitOffsetPagination

     class MyLimitOffsetPagination(LimitOffsetPagination):
         default_limit = 10  # Default number of results per request
         max_limit = 100  # Maximum limit for results

     # In your view
     from rest_framework.views import APIView
     from rest_framework.response import Response

     class MyAPIView(APIView):
         pagination_class = MyLimitOffsetPagination

         def get(self, request):
             queryset = MyModel.objects.all()
             paginator = self.pagination_class()
             page = paginator.paginate_queryset(queryset, request)
             return paginator.get_paginated_response(page)
     ```

3. **CursorPagination**:
   - This style is based on a cursor (a unique field, such as an ID), allowing more efficient pagination by providing a pointer to the next set of results.
   - **Usage**:
     ```python
     from rest_framework.pagination import CursorPagination

     class MyCursorPagination(CursorPagination):
         page_size = 10  # Default number of results per page
         ordering = 'created'  # Field to order by

     # In your view
     from rest_framework.views import APIView
     from rest_framework.response import Response

     class MyAPIView(APIView):
         pagination_class = MyCursorPagination

         def get(self, request):
             queryset = MyModel.objects.all()
             paginator = self.pagination_class()
             page = paginator.paginate_queryset(queryset, request)
             return paginator.get_paginated_response(page)
     ```

### Configuring Pagination Globally

You can also set default pagination settings in your `settings.py` file, which will apply to all your views unless overridden:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### Pagination and ViewSet

```python
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductSerializer

class ProductPagination(PageNumberPagination):
    page_size = 5  # Number of items per page
    page_size_query_param = 'page_size'  # Allows clients to set page size
    max_page_size = 10  # Maximum page size limit

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

```

### Using Pagination

- **PageNumberPagination**: You can navigate through pages using the query parameters:
  - `/api/my-endpoint/?page=2`
  - `/api/my-endpoint/?page_size=5`

- **LimitOffsetPagination**: Use the following parameters:
  - `/api/my-endpoint/?limit=10&offset=20`

- **CursorPagination**: The response will contain a `next` and `previous` field with encoded cursors to navigate through the pages.

### Conclusion

Pagination is a crucial aspect of API design that enhances performance and user experience.
Django REST Framework provides flexible options to implement pagination according to your needs. 
You can choose the pagination style that best fits your application requirements and configure it globally or on a per-view basis.
