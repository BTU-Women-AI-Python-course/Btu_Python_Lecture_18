# Custom Permissions in Django REST Framework

Permissions in DRF control whether a user can access or modify a specific view. DRF provides built-in permissions, but in many cases, custom permissions are necessary.

To create a custom permission, you need to define a class that inherits from `BasePermission` and override the `has_permission` or `has_object_permission` methods.

### Structure of Custom Permission

A custom permission class typically looks like this:

```python
from rest_framework.permissions import BasePermission

class MyCustomPermission(BasePermission):
    def has_permission(self, request, view):
        # Custom logic for general access to the view
        return True or False
    
    def has_object_permission(self, request, view, obj):
        # Custom logic for specific object-level access
        return True or False
```

The `has_permission` method is for checking general access to the view, and `has_object_permission` is for checking permissions on a specific object (instance).

### Example 1: Admin-Only Permission

This permission allows access to the view only if the user is an admin.

```python
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
```

Usage in a view:

```python
from rest_framework.views import APIView
from .permissions import IsAdminUser

class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"message": "You are an admin!"})
```

### Example 2: Permission Based on User Group

This permission checks if the user belongs to a specific group (e.g., `editors`).

```python
from rest_framework.permissions import BasePermission

class IsEditorUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='editors').exists()
```

Usage in a view:

```python
from rest_framework.views import APIView
from .permissions import IsEditorUser

class EditorOnlyView(APIView):
    permission_classes = [IsEditorUser]

    def get(self, request):
        return Response({"message": "You are an editor!"})
```

### Example 3: Object-Level Permission (Owner-Only Access)

This permission allows users to access or modify objects only if they are the owner of the object.

```python
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Assumes the object has an 'owner' attribute
        return obj.owner == request.user
```

Usage in a view:

```python
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import MyModel
from .permissions import IsOwner

class MyModelDetailView(RetrieveUpdateDestroyAPIView):
    queryset = MyModel.objects.all()
    permission_classes = [IsOwner]
    serializer_class = MyModelSerializer
```

### Example 4: Custom Logic Based on HTTP Methods

This permission grants `SAFE_METHODS` (`GET`, `HEAD`, `OPTIONS`) to all users but restricts `POST`, `PUT`, and `DELETE` to admins only.

```python
from rest_framework.permissions import BasePermission, SAFE_METHODS

class ReadOnlyOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # Allow GET, HEAD, OPTIONS for any user
        return request.user.is_staff  # Allow POST, PUT, DELETE only for admin users
```

Usage in a view:

```python
from rest_framework.views import APIView
from .permissions import ReadOnlyOrAdmin

class MyView(APIView):
    permission_classes = [ReadOnlyOrAdmin]

    def get(self, request):
        return Response({"message": "This is a read-only view."})
    
    def post(self, request):
        return Response({"message": "Admin-only action."})
```

### Example 5: Combination of Multiple Permissions

Sometimes, you may want to combine multiple custom permissions. For example, users need to be both admins and owners of the object.

```python
from rest_framework.permissions import BasePermission

class IsAdminAndOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff and obj.owner == request.user
```

Usage in a view:

```python
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import MyModel
from .permissions import IsAdminAndOwner

class AdminAndOwnerView(RetrieveUpdateDestroyAPIView):
    queryset = MyModel.objects.all()
    permission_classes = [IsAdminAndOwner]
    serializer_class = MyModelSerializer
```

### Example 6: Permission Based on a Custom User Attribute

In some cases, permissions can be based on custom user attributes. For example, if a user has a boolean `can_edit` field, the permission would look like this:

```python
from rest_framework.permissions import BasePermission

class CanEditPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.can_edit
```

Usage in a view:

```python
from rest_framework.views import APIView
from .permissions import CanEditPermission

class EditView(APIView):
    permission_classes = [CanEditPermission]

    def post(self, request):
        return Response({"message": "You have permission to edit!"})
```

---

### Applying Custom Permissions Globally

If you want to apply the same permission to every view in the project, you can configure it in the `settings.py` file.

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'myapp.permissions.IsAdminUser',
    ],
}
```

This will make `IsAdminUser` the default permission for all views unless overridden at the view level.

### Conclusion

Custom permissions in Django REST Framework allow you to implement fine-grained access control
tailored to your application's needs. By creating classes that inherit from `BasePermission`,
you can customize both general view access and object-specific access.
