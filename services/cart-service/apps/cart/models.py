from turtle import mode
from django.db import models

class Cart(models.Model):

    user_id = models.IntegerField(unique = True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"Корзина пользователя с id: {self.user_id}"
    
    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def clear(self):
        self.items.all().delete()

class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField(default = 1)
    product_name = models.CharField(max_length = 255)
    product_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = ['cart', 'product_id']
    
    def __str__(self):
        return f"{self.cart} {self.product_name}"
    
    @property
    def subtotal(self):
        return self.product_price * self.quantity
        