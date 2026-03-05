from rest_framework import serializers

from .models import Category, Product, ProductImage, SliderImage

class SliderImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = SliderImage
        fields = ['id', 'title', 'description', 'image_url', 'link', 'order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

class CategorySerializer(serializers.ModelSerializer):

    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'created_at', 'products_count', 'updated_at')

    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductCardSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(source='category.name', read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category_name', 'price', 'stock_quantity', 'main_image', 'is_in_stock', 'created_at', 'updated_at')

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('id', 'image')

class ProductDetailSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(source='category.name', read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category_name', 'price', 'stock_quantity', 'is_in_stock', 'images', 'created_at', 'updated_at', 'is_active')
        
        