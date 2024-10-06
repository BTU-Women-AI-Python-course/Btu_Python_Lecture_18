from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.serializers import UserSerializer
from users.filters import UserFilter
from users.permissions import IsAuthenticatedUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [IsAuthenticatedUser]

    @action(detail=True, methods=['get'])
    def get_username_only(self, request, pk=None):
        user = self.get_object()
        return Response({'username': user.username})

