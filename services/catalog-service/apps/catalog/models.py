from django.db import models
from django.utils.text import slugify

class Category(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    main_image = models.ImageField(upload_to='products/main/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    def remove_from_stock(self, quantity):
        """Удаление из скалада при заказе"""
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
            return True
        return False
    
    def return_to_stock(self, quntity):
        """Возвращение на склад при отмене заказа"""
        self.stock_quantity += quntity
        self.save()
    
class ProductImage(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/extra/', blank=True, null=True)