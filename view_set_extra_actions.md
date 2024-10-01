# Rest Framework - ViewSet Extra Actions

In Django REST Framework (DRF), `ViewSet` classes allow you to group related views (actions) together. By default, a `ViewSet` provides actions like `list`, `retrieve`, `create`, `update`, and `destroy`. However, you might want to add custom actions to a `ViewSet` that are not directly tied to these CRUD operations. This is where **extra actions** come into play.

### Extra Actions in ViewSets
Extra actions are custom methods in a `ViewSet` that you can expose as additional endpoints. You define these actions using the `@action` decorator from `rest_framework.decorators`.

Here's a step-by-step guide on how to use extra actions in a `ViewSet`:

### Step 1: Import the `@action` Decorator
To define an extra action, first, you need to import the `@action` decorator from `rest_framework`.

```python
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import Product
from .serializers import ProductPriceUpdateSerializer
```

### Step 2: Define a ViewSet with Extra Actions Using Serializer
Create a custom `ProductViewSet` and define the extra actions using the `@action` decorator. Here, we use the `ProductPriceUpdateSerializer` to handle the `set_price` action.

```python
class ProductViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='set-price', url_name='set-price')
    def set_price(self, request):
        # Use the serializer to validate the input data
        serializer = ProductPriceUpdateSerializer(data=request.data)
        if serializer.is_valid():
            # Retrieve validated data
            product_id = serializer.validated_data['product_id']
            new_price = serializer.validated_data['new_price']

            # Update the price of the specified product
            try:
                product = Product.objects.get(id=product_id)
                product.price = new_price
                product.save()
                return Response({'status': f'Price set to {new_price} for product {product.name}'})
            except Product.DoesNotExist:
                return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Step 3: Use the `@action` Decorator
The `@action` decorator has several parameters:

- **`detail`**: A boolean that specifies if the action is intended for a single object (`detail=True`) or the entire list (`detail=False`).
- **`methods`**: A list of HTTP methods allowed for this action (e.g., `['get', 'post']`).
- **`url_path`**: An optional parameter to specify a custom URL for the action.
- **`url_name`**: An optional parameter to specify a custom name for the action.

### Example: Extra Action with Serializer
```python
class ProductViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='set-price', url_name='set-price')
    def set_price(self, request):
        # This action can be accessed via /products/set-price/
        serializer = ProductPriceUpdateSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            new_price = serializer.validated_data['new_price']
            try:
                product = Product.objects.get(id=product_id)
                product.price = new_price
                product.save()
                return Response({'status': f'Price set to {new_price} for product {product.name}'})
            except Product.DoesNotExist:
                return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Step 4: Register the ViewSet in the Router
Make sure to register your `ProductViewSet` with a router in your `urls.py` file.

```python
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
urlpatterns = router.urls
```

### Step 5: Access the Extra Actions
Once your `ViewSet` is registered with the router, you can access the extra actions via the defined URLs:

- If `detail=True`:
  - `/products/{id}/details/`
- If `detail=False`:
  - `/products/set-price/`

### Using `@action` in ViewSets for the `Product` Model

```python
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer, ProductPriceUpdateSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def latest_products(self, request):
        """
        This action retrieves a list of the latest products added.
        Accessed via /products/latest_products/
        """
        latest_products = self.get_queryset().order_by('-created_at')[:5]
        serializer = self.get_serializer(latest_products, many=True)
        return Response(serializer.data)
```

### Best Practices and Tips
1. **Naming Conventions**: Use meaningful names for your extra actions and URL paths to keep the API self-documenting.
2. **Permissions and Authentication**: Ensure that you configure permissions and authentication on your custom actions. You can use the `@permission_classes` and `@authentication_classes` decorators.
3. **Detail vs. Non-Detail Actions**: Choose the appropriate `detail` parameter value. If an action operates on a single object, set `detail=True`. If it's a list-level action, set `detail=False`.
