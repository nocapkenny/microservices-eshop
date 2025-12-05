import httpx
import json
import logging
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class ProxyView(View):
    """Асинхронный прокси к микросервисам"""

    async def dispatch(self, request, *args, **kwargs):
        logger.info(f"Async gateway request: {request.method} {request.path}")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Body: {request.body.decode('utf-8') if request.body else 'No body'}")

        service_name = self.get_service_name(request)
        if not service_name:
            logger.error(f"Service not found for path: {request.path}")
            return JsonResponse({'error': 'Service not found'}, status=404)

        service_url = settings.MICROSERVICES.get(service_name)
        if not service_url:
            logger.error(f"Service {service_name} not configured")
            return JsonResponse({'error': f'Service {service_name} not configured'}, status=500)

        target_path = self.get_target_path(request)
        target_url = f"{service_url}{target_path}"
        logger.info(f"Proxying to: {target_url}")

        return await self.proxy_request(request, target_url)

    def get_service_name(self, request):
        path = request.path
        if path.startswith('/api/user/'):
            return 'user-service'
        elif path.startswith('/api/products/') or path.startswith('/api/categories/'):
            return 'product-service'
        elif path.startswith('/api/cart/'):
            return 'cart-service'
        elif path.startswith('/api/order/'):
            return 'order-service'
        return None

    def get_target_path(self, request):
        path = request.path
        if path.startswith('/api/'):
            return path
        return path

    async def proxy_request(self, request, target_url):
        print(">>> Proxying request...", target_url)
        try:
            headers = {}
            important_headers = [
                'Authorization', 'Content-Type', 'Accept', 'User-Agent',
                'Accept-Language', 'Accept-Encoding'
            ]
            for h in important_headers:
                val = request.headers.get(h)
                if val:
                    headers[h] = val

            logger.info(f"Forwarding headers: {headers}")

            # Обработка тела запроса
            content = None
            json_data = None

            if request.method in ['POST', 'PUT', 'PATCH']:
                content_type = request.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    try:
                        if request.body:
                            json_data = json.loads(request.body.decode('utf-8'))
                            logger.info(f"JSON data: {json_data}")
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        logger.error(f"Failed to parse JSON: {e}")
                        content = request.body
                else:
                    content = request.body

            # Query параметры
            params = dict(request.GET.items())
            if params:
                logger.info(f"Query params: {params}")

            # Асинхронный запрос через httpx
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.request(
                    method=request.method,
                    url=target_url,
                    headers=headers,
                    json=json_data,
                    content=content,
                    params=params,
                )

            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response content: {response.text[:200]}...")

            # Возвращаем ответ
            django_response = HttpResponse(
                response.content,
                status=response.status_code,
                content_type=response.headers.get('content-type', 'application/json')
            )

            for key in ['Content-Type', 'Cache-Control', 'ETag']:
                if key in response.headers:
                    django_response[key] = response.headers[key]

            return django_response

        except httpx.TimeoutException:
            logger.error(f"Timeout when calling {target_url}")
            return JsonResponse({'error': 'Service timeout'}, status=504)
        except httpx.NetworkError as e:
            logger.error(f"Connection error when calling {target_url}: {e}")
            return JsonResponse({'error': 'Service unavailable'}, status=503)
        except Exception as e:
            logger.error(f"Error proxying request to {target_url}: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)


proxy_view = ProxyView.as_view()