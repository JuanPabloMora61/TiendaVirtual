from django.db import models
from .forms import *


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'Categoría: {self.name}'

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def category_name(self):
        return self.category.name

# Shopping Cart Models

class Cart(models.Model):
    pass

    class Meta:
        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'
    
    def __str__(self):
        return f'Shopping Cart {self.id}'
    
    @property
    def total_items(self):
        return self.items.count()

    @property
    def total_price(self):
        return sum([item.total_price for item in self.items.all()])

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'Shopping Cart Item'
        verbose_name_plural = 'Shopping Cart Items'
    
    def __str__(self):
        return self.product.name
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    def get_form(self, data=None):
        initial = {'quantity': self.quantity}
        return CartAddProductForm(initial = initial)