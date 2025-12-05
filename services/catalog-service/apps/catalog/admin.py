from django.contrib import admin

from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock_quantity', 'is_active')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    list_filter = ('product__category',)


