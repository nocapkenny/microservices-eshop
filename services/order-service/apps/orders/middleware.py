import jwt
from django.http import JsonResponse
from django.conf import settings
from .services import AuthService
import logging
import re

logger = logging.getLogger(__name__)


class JWTAuthenticationMiddleware:
    """
    Middleware для аутентификации через JWT токены.
    Пропускает публичные эндпоинты: админка, статика, медиа, авторизация, публичные API.
    """

    # Пути, не требующие аутентификации
    PUBLIC_PATHS = [
        '/admin/',
        '/static/',
        '/media/',
        '/health/',
        '/api/auth/',          # Логин, регистрация, refresh
        '/api/slider/',        # Публичный слайдер
        '/api/catalog/',       # Публичный каталог
        '/api/products/',      # Публичные товары
        '/api/categories/',    # Публичные категории
        '/api/search/',        # Поиск
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Пропускаем публичные пути
        if self._is_public_path(request.path):
            return self.get_response(request)

        # 2. Пропускаем preflight запросы (CORS)
        if request.method == 'OPTIONS':
            return self.get_response(request)

        # 3. Проверяем наличие токена
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            logger.warning(f"No auth header found for {request.path}")
            return JsonResponse({
                'error': 'Authentication required',
                'message': 'Authorization header with Bearer token is required'
            }, status=401)

        # 4. Валидируем токен
        token = auth_header.split(' ')[1]
        logger.info(f"Validating token for request to {request.path}")

        user_data = AuthService.get_user_from_token(token)
        
        if user_data:
            # Сохраняем данные пользователя в запрос
            request.user_id = user_data['id']
            request.user_email = user_data['email']
            request.user_is_authenticated = True  # Флаг для удобства
            logger.info(f"✓ Authenticated user {user_data['id']} for {request.path}")
            return self.get_response(request)
        else:
            logger.warning(f"✗ Invalid token for {request.path}")
            return JsonResponse({
                'error': 'Invalid token',
                'message': 'The provided authentication token is invalid or expired'
            }, status=401)

    def _is_public_path(self, path: str) -> bool:
        """
        Проверяет, является ли путь публичным (не требует аутентификации).
        Использует startswith для корректной работы с вложенными путями.
        """
        # Нормализуем путь (убираем трейлинг слэш для сравнения)
        normalized_path = path.rstrip('/') + '/'
        
        for public_path in self.PUBLIC_PATHS:
            # Нормализуем и сравниваемый путь
            normalized_public = public_path.rstrip('/') + '/'
            if normalized_path.startswith(normalized_public):
                return True
        
        # Дополнительно: регулярные выражения для сложных случаев
        # Например, любые эндпоинты с параметрами: /api/products/123/
        public_patterns = [
            r'^/api/products/\d+/?$',      # /api/products/123/
            r'^/api/categories/\d+/?$',    # /api/categories/5/
            r'^/api/catalog/\d+/?$',       # /api/catalog/42/
        ]
        for pattern in public_patterns:
            if re.match(pattern, path):
                return True
                
        return False