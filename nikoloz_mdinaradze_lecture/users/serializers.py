from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def validate(self, attrs):
        if password := attrs.get('password'):
            attrs['password'] = make_password(password)
        return attrs
