
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import CustomUser

# from djoser.serializers import ActivationEmail

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'code', 'code_expiry', 'code_attempts', 'password')



