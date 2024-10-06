from django.contrib.auth.models import User
from rest_framework import viewsets

from users.serializers import UserSerializer
from users.filters import UserFilter

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter

