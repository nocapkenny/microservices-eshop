from rest_framework import serializers

from .models import Cart, CartItem
from .services import CatalogService, AuthService


class CartItemSerializer(serializers.ModelSerializer):

    subtotal = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    product_info = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity",
                  "product_name", "product_price", "product_info", "subtotal", "created_at", "updated_at"]

    def get_product_info(self, obj):

        product_data = CatalogService.get_product(obj.product_id)
        if product_data:
            return {
                'name': product_data.get('name'),
                'current_price': product_data.get('price'),
                'is_active': product_data.get('is_active'),
                'stock_quantity': product_data.get('stock_quantity'),
            }
        return None


class CartSerializer(serializers.ModelSerializer):
    # related name не указан в модели, используем default cartitem_set
    items = CartItemSerializer(many=True, read_only=True)

    total_amount = serializers.DecimalField(max_digits=10,
                                            decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user_id", "created_at", "updated_at", "items", 'total_amount',
            'total_items']
        read_only_fields = ["id", "created_at", "updated_at", "items"]


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_product_id(self, value):
        """Проверка существования товара"""
        product_data = CatalogService.get_product(value)
        if not product_data:
            raise serializers.ValidationError("Product not found")
        if not product_data.get('is_active'):
            raise serializers.ValidationError("Product is not active")
        return value


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество должно быть не меньше 1")
        
        # Проверка остатков
        cart_item = self.instance
        if cart_item:
            product_data = CatalogService.get_product(cart_item.product_id)
            if product_data:
                stock = product_data.get('stock_quantity', 0)
                if value > stock:
                    raise serializers.ValidationError(
                        f"На складе осталось только {stock} шт."
                    )
        return value
