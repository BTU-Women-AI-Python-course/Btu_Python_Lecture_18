# Django rest Framework Filters

Django REST Framework (DRF) provides powerful capabilities for filtering querysets,
allowing clients to retrieve specific subsets of data from your APIs. This is essential for creating flexible and user-friendly APIs.

### Setting Up Django Filters

To use filters in DRF, you typically need to install the `django-filter` package, which provides the filtering capabilities.

1. **Install django-filter**:
   ```bash
   pip install django-filter
   ```

2. **Add it to your `INSTALLED_APPS`** in `settings.py`:
   ```python
   INSTALLED_APPS = [
       ...
       'django_filters',
   ]
   ```

3. **Configure DRF to use Django Filters**:
   ```python
   # settings.py
   REST_FRAMEWORK = {
       'DEFAULT_FILTER_BACKENDS': (
           'django_filters.rest_framework.DjangoFilterBackend',
           ...
       ),
   }
   ```

### Basic Filtering

To enable basic filtering on your views, you can use `FilterSet`. Here’s how to set it up:

1. **Create a FilterSet**:
   ```python
   from django_filters import rest_framework as filters
   from .models import MyModel

   class MyModelFilter(filters.FilterSet):
       name = filters.CharFilter(lookup_expr='icontains')  # Filter for case-insensitive match
       created_after = filters.DateFilter(field_name='created_at', lookup_expr='gte')  # Filter for date

       class Meta:
           model = MyModel
           fields = ['name', 'created_after']
   ```

2. **Apply the FilterSet to a View**:
   ```python
   from rest_framework import viewsets
   from .models import MyModel
   from .serializers import MyModelSerializer
   from .filters import MyModelFilter

   class MyModelViewSet(viewsets.ModelViewSet):
       queryset = MyModel.objects.all()
       serializer_class = MyModelSerializer
       filterset_class = MyModelFilter
   ```

### Example API Call

With the above setup, you can now filter your API results using query parameters. For example:

- To filter by name:
  ```
  GET /api/my-models/?name=example
  ```

- To filter by creation date:
  ```
  GET /api/my-models/?created_after=2023-01-01
  ```

### Advanced Filtering

You can also implement more complex filtering logic, such as filtering by multiple fields or using custom filter methods.

1. **Custom Filter Method**:
   ```python
   from django_filters import rest_framework as filters
   from .models import MyModel

   class MyModelFilter(filters.FilterSet):
       custom_field = filters.CharFilter(method='filter_custom_field')

       class Meta:
           model = MyModel
           fields = ['custom_field']

       def filter_custom_field(self, queryset, name, value):
           return queryset.filter(another_field__contains=value)  # Custom filtering logic
   ```

### Filtering with Query Parameters

You can also use the `DjangoFilterBackend` to filter your results with a variety of query parameters. Common filter operations include:

- **Exact Match**: 
  - `GET /api/my-models/?name=John`

- **Case-insensitive Match**:
  - `GET /api/my-models/?name__icontains=jo`

- **Date Filtering**:
  - `GET /api/my-models/?created_at__gte=2023-01-01` (greater than or equal to)
  - `GET /api/my-models/?created_at__lt=2023-12-31` (less than)

### Conclusion

Django filters in the REST framework provide a powerful way to customize the data returned by your API. 
By using `django-filter`, you can easily create flexible filters to meet your application's needs. 
Remember to explore the extensive filtering capabilities offered by `django-filter` to enhance your API's functionality.
