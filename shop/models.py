from django.db import models
from .forms import *


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'Categoría: {self.name}'
    
class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return f'Tags: {self.name}'

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre del Producto')
    description = models.TextField('Descripción del producto')
    price = models.IntegerField('Precio del producto')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Categoría')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products', blank=True, null=True, verbose_name='Imagen', help_text='La imagen debe tener un tamaño de 300x300px')
    tag = models.ManyToManyField(Tag, related_name='products', help_text='Da doble click para seleccionar un tag')

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