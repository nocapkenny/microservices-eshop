from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, UserUpdateSerializer



class UserProfileView(generics.RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class  = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Аутентификация пользователя
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Email и пароль обязательны'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=email, password=password)
    if user and user.is_active:
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': user_serializer.data
        })

    return Response(
        {'error': 'Неверные учетные данные'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    Обновление access token
    """
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken(refresh_token)
        return Response({
            'access': str(refresh.access_token),
        })
    except Exception as e:
        return Response(
            {'error': 'Неверный refresh token'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Регистрация нового пользователя
    """
    from .serializers import UserRegistrationSerializer
    
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': user_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
