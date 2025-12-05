from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для базовой информации о пользователе
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name',
                 'phone', 'date_of_birth', 'avatar', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'is_active']
    
    def get_full_name(self, obj):
        """Получение полного имени пользователя"""
        return obj.get_full_name()

class UserDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детальной информации о пользователе (включая служебные поля)
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name',
                 'phone', 'date_of_birth', 'avatar', 'is_active', 'is_staff', 
                 'is_superuser', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser']
    
    def get_full_name(self, obj):
        """Получение полного имени пользователя"""
        return obj.get_full_name()

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления информации о пользователе
    """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'date_of_birth', 'avatar']
        read_only_fields = ['email']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'date_of_birth', 
                 'password', 'password_confirm']

    def validate_email(self, value):
        """Проверка уникальности email"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    def validate_password(self, value):
        """Валидация пароля"""
        try:
            validate_password(value)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        """Проверка совпадения паролей"""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': 'Пароли не совпадают'
            })
        return attrs

    def create(self, validated_data):
        """Создание пользователя"""
        # Убираем password_confirm из данных
        validated_data.pop('password_confirm', None)

        # Создаем пользователя
        user = User.objects.create_user(**validated_data)
        return user
