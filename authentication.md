# Dajngo Rest Framework Authentication

Django REST Framework (DRF) provides several authentication methods to secure your APIs. 
Authentication is the process of verifying the identity of a user, and DRF supports
various authentication classes out of the box, which can be easily configured to meet your needs.

### Authentication Methods in Django REST Framework

1. **Session Authentication**:
   - This is the default authentication method in DRF, relying on Django's session framework. It uses session IDs stored in cookies.
   - **Usage**:
     ```python
     from rest_framework.views import APIView
     from rest_framework.response import Response
     from rest_framework.permissions import IsAuthenticated

     class MyAPIView(APIView):
         permission_classes = [IsAuthenticated]

         def get(self, request):
             return Response({"message": "Hello, authenticated user!"})
     ```

2. **Token Authentication**:
   - This method uses tokens to authenticate users. A token is generated for each user and is included in the request header for authentication.
   - **Setup**:
     1. Install the `djangorestframework` package if you haven't already:
        ```bash
        pip install djangorestframework
        ```
     2. Add `rest_framework.authtoken` to your `INSTALLED_APPS` in `settings.py`:
        ```python
        INSTALLED_APPS = [
            ...
            'rest_framework.authtoken',
        ]
        ```
     3. Run migrations:
        ```bash
        python manage.py migrate
        ```
     4. Create a token for users (usually in a view or via the Django admin):
        ```python
        from rest_framework.authtoken.models import Token
        from django.contrib.auth.models import User

        user = User.objects.get(username='your_username')
        token = Token.objects.create(user=user)
        print(token.key)  # This is the token to use for authentication
        ```

   - **Usage in View**:
     ```python
     from rest_framework.authentication import TokenAuthentication
     from rest_framework.permissions import IsAuthenticated
     from rest_framework.views import APIView
     from rest_framework.response import Response

     class MyAPIView(APIView):
         authentication_classes = [TokenAuthentication]
         permission_classes = [IsAuthenticated]

         def get(self, request):
             return Response({"message": "Hello, authenticated user!"})
     ```

   - **Making Requests**:
     Include the token in the request header:
     ```
     Authorization: Token your_token_here
     ```

3. **Basic Authentication**:
   - This method uses HTTP Basic Authentication, where the user's credentials (username and password) are sent in the request header.
   - **Usage**:
     ```python
     from rest_framework.authentication import BasicAuthentication
     from rest_framework.permissions import IsAuthenticated
     from rest_framework.views import APIView
     from rest_framework.response import Response

     class MyAPIView(APIView):
         authentication_classes = [BasicAuthentication]
         permission_classes = [IsAuthenticated]

         def get(self, request):
             return Response({"message": "Hello, authenticated user!"})
     ```

   - **Making Requests**:
     Include the credentials in the request header:
     ```
     Authorization: Basic base64(username:password)
     ```

4. **JWT Authentication**:
   - JSON Web Tokens (JWT) are another popular authentication method for APIs. You can use the `djangorestframework-simplejwt` package to implement JWT authentication.
   - **Setup**:
     1. Install the package:
        ```bash
        pip install djangorestframework-simplejwt
        ```
     2. Configure it in `settings.py`:
        ```python
        REST_FRAMEWORK = {
            'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework_simplejwt.authentication.JWTAuthentication',
            ),
        }
        ```

   - **Getting a Token**:
     Create a view to obtain the JWT token:
     ```python
     from rest_framework_simplejwt.views import TokenObtainPairView

     urlpatterns = [
         path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
         path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
         path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
     ]
     ```

   - **Using the Token**:
     When you make a POST request to `/api/token/` with valid user credentials, you will receive an access and refresh token:
     ```json
     {
         "access": "your_access_token",
         "refresh": "your_refresh_token"
     }
     ```

   - **Making Requests**:
     Include the access token in the request header:
     ```
     Authorization: Bearer your_access_token
     ```

### Conclusion

Django REST Framework provides multiple authentication methods, allowing you to choose the one that best suits your application's requirements. 
From session and token-based authentication to JWT, each method has its use cases and configurations.
Make sure to choose the appropriate authentication strategy based on your security and usability needs.
