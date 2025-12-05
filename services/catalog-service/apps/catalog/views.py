from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductCardSerializer, ProductDetailSerializer, ProductImageSerializer


class CategoryListView(generics.ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class ProductCardView(generics.ListAPIView):

    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductCardSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('category',)
    search_fields = ('name', 'description')
    ordering_fields = ('price', 'created_at')
    ordering = ('-created_at') 

    def get_queryset(self):
        
        queryset = super().get_queryset()

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        in_stock = self.request.query_params.get('in_stock')
        if in_stock and in_stock.lower() == 'true':
            queryset = queryset.filter(stock_quantity__gt=0)

        return queryset

class ProductDetailView(generics.RetrieveAPIView):

    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer


class ProductsByCategoryView(generics.ListAPIView):

    serializer_class = ProductCardSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ('name', 'description')
    ordering_fields = ('price', 'created_at')
    ordering = ('-created_at')

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug)
        queryset = Product.objects.filter(category=category, is_active=True)
        

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        in_stock = self.request.query_params.get('in_stock')
        if in_stock and in_stock.lower() == 'true':
            queryset = queryset.filter(stock_quantity__gt=0)

        return queryset

@api_view(['POST'])
def reserve_product(request, product_id):
    """Резервирование товара для заказа"""
    try:
        product = Product.objects.get(id=product_id)
        quantity = request.data.get('quantity', 1)

        if product.remove_from_stock(quantity):
            return Response({
                'success': True,
                'message': f'Reserved {quantity} units of {product.name}',
                'remaining_stock': product.stock_quantity
            })
        else:
            return Response({
                'success': False,
                'message': 'Insufficient stock',
                'available_stock': product.stock_quantity
            }, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Product not found'
        }, status=status.HTTP_404_NOT_FOUND)