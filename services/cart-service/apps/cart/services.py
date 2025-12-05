import requests
import logging
from django.conf import settings
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class CatalogService:
    """Сервис для взаимодействия с Catalog Service"""

    @staticmethod
    def get_product(product_id: int) -> Optional[Dict[str, Any]]:
        """Получение информации о товаре"""
        try:
            response = requests.get(
                f"{settings.CATALOG_SERVICE_URL}/api/products/{product_id}/",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get product {product_id}: {e}")
            return None

class AuthService:
    """Сервис для взаимодействия с Auth Service"""

    @staticmethod
    def get_user_from_token(token: str) -> Optional[Dict[str, Any]]:
        """Получение информации о пользователе по токену"""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(
                f"{settings.USER_SERVICE_URL}/api/user/profile/",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get user from token: {e}")
            return None
