from django.urls import path
from .views import CategoryListView, ProductCardView, ProductDetailView, ProductsByCategoryView, reserve_product

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('products/', ProductCardView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    path('products/<slug:category_slug>/', ProductsByCategoryView.as_view()),
    path('products/<int:product_id>/remove/', reserve_product)
]