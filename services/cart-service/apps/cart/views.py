from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, AddToCartSerializer, UpdateCartItemSerializer
from .services import CatalogService

class IsAuthenticatedCustom:

    def has_permission(self, request, view):
        return hasattr(request, 'user_id') and request.user_id is not None
    def has_object_permission(self, request, view, obj):
        # Доступ к объекту уже ограничен get_queryset(),
        # поэтому просто разрешаем, если пользователь аутентифицирован
        return self.has_permission(request, view)
    
class CartView(generics.RetrieveAPIView):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user_id=self.request.user_id)
        return cart

class CartAddItemView(generics.CreateAPIView):
    """
    Добавление или обновление товара в корзине.
    """
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticatedCustom]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        
        cart, _ = Cart.objects.get_or_create(user_id=request.user_id)


        product_data = CatalogService.get_product(product_id)
        if not product_data:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={
                'quantity': quantity,
                'product_price': product_data['price'],
                'product_name': product_data['name']
            }
        )

        if not created:

            new_quantity = cart_item.quantity + quantity

            cart_item.quantity = new_quantity
            cart_item.save()

        return Response(
            {
                'message': 'Product added to cart successfully',
                'cart_item': CartItemSerializer(cart_item).data
            },
            status=status.HTTP_201_CREATED
        )

class CartClearAPIView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        # 1. Получаем user_id из аутентификации
        user_id = getattr(request, 'user_id', None)
        if user_id is None:
            return Response(
                {"detail": "User not authenticated"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 2. Находим или создаём корзину (на случай, если её нет)
        cart = Cart.objects.filter(user_id=user_id).first()
        if cart is None:
            # Нет корзины — считаем, что она и так "очищена"
            return Response(status=status.HTTP_204_NO_CONTENT)

        # 3. Удаляем все элементы
        try:
            cart.items.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            # Логируем ошибку (в продакшене — через logging)
            print(f"Error clearing cart for user {user_id}: {e}")
            return Response(
                {"detail": "Internal error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CartItemDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        user_id = getattr(self.request, 'user_id', None)
        return CartItem.objects.filter(cart__user_id=user_id)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        cart = instance.cart
        instance.delete()

        # Возвращаем обновлённую корзину
        cart_data = CartSerializer(cart).data
        return Response(cart_data, status=status.HTTP_200_OK)


class CartItemUpdateView(generics.UpdateAPIView):
    """Обновление количества элемента корзины."""
    serializer_class = UpdateCartItemSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        user_id = getattr(self.request, 'user_id', None)
        return CartItem.objects.filter(cart__user_id=user_id)

    def update(self, request, *args, **kwargs):
        # Стандартное обновление
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Получаем обновлённую корзину целиком
        cart = instance.cart
        cart_data = CartSerializer(cart).data
        return Response(cart_data, status=status.HTTP_200_OK)

