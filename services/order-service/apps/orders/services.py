import requests
import logging
import redis
import json

from typing import Optional, Dict, Any, List
from django.conf import settings

logger = logging.getLogger(__name__)


class EventBus:
    """Сервис для публикации событий"""

    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )

    def publish_event(self, event_type: str, data: Dict[str, Any]):
        """Публикация события"""
        try:
            event_data = {
                'type': event_type,
                'data': data,
                'timestamp': json.dumps({}, default=str)
            }
            self.redis_client.publish('events', json.dumps(event_data, default=str))
            logger.info(f"Published event: {event_type}")
        except Exception as e:
            logger.error(f"Failed to publish event {event_type}: {e}")

event_bus = EventBus()

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
        
    @staticmethod
    def remove_product(items: List[Dict]) -> bool:
        
        try:
            for item in items:
                response = requests.post(
                    f"{settings.CATALOG_SERVICE_URL}/api/products/{item['product_id']}/remove/",
                    json={'quantity': item['quantity']},
                    timeout=10
                )
                if response.status_code != 200:
                    return False
            return True
        except requests.exceptions.RequestException as e:
            return False
    
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

class CartService:
    """Сервис для взаимодействия с Cart Service"""

    @staticmethod
    def get_user_cart(user_id: int, token: str) -> Optional[Dict[str, Any]]:
        """Получение корзины пользователя"""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(
                f"{settings.CART_SERVICE_URL}/api/cart/",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get cart for user {user_id}: {e}")
            return None