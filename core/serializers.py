from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

# USER_MODEL = get_user_model()
from core.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя посредством пароля"""
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        """Переопределение пустого validate для проверки пароля и удаление password_repeat"""
        password = attrs.get('password')
        password_repeat = attrs.pop('password_repeat')

        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({'password': e.messages})

        if password_repeat != password:
            raise serializers.ValidationError({'password': "Passwords do not match. Пароли не совпадают."})
        return attrs

    def create(self, validated_data: dict) -> User:
        password = validated_data.get('password')
        validated_data['password'] = make_password(password)
        instance = super().create(validated_data)
        return instance

    class Meta:
        model = User
        fields = "__all__"


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data: dict) -> User:
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password']
        )
        if not user:
            raise AuthenticationFailed
        return user

    class Meta:
        model = User
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class UpdatePasswordSerializer(serializers.Serializer):
    """Сериализатор по обновлению пароля пользователя"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: dict) -> dict:
        """Переопределение пустого validate для проверки пароля и удаление password_repeat"""
        user = attrs['user']
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({'old_password': 'incorrect password - Неверный пароль'})
        try:
            validate_password(attrs['new_password'])
        except Exception as e:
            raise serializers.ValidationError({'new_password': e.messages})
        return attrs

    def update(self, instance: User, validated_data: dict) -> User:
        instance.password = make_password(validated_data['new_password'])
        instance.save()
        return instance
