from django.contrib.sites import requests
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model, login, logout
from . import serializers
from .models import User


class RegistrationView(generics.CreateAPIView):
    """Класс для регистрации пользователя, использующий сериализатор из 'serializer_class'"""
    model = User
    serializer_class = serializers.RegistrationSerializer


class LoginView(generics.CreateAPIView):
    """Класс для входа пользователя, использующий сериализатор из 'serializer_class',
            проверяющий валидность введенных данных"""
    model = User
    serializer_class = serializers.LoginSerializer

    def post(self, request: requests, *args: str, **kwargs: int) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """Класс для просмотра профиля пользователя, использующий сериализатор из 'serializer_class',
            модель 'USER_MODEL' и выданные разрешения (permission_classes)"""
    serializer_class = serializers.ProfileSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user

    def delete(self, request: requests, *args: str, **kwargs: int) -> Response:
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(generics.UpdateAPIView):
    """Класс для изменения текущего пароля на новый, использующий сериализатор из 'serializer_class'
            и выданные разрешения (permission_classes)"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UpdatePasswordSerializer

    def get_object(self) -> User:
        return self.request.user
