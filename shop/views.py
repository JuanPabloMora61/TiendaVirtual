from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import CreateView
from django import forms

from shop.models import *
from shop.utils import get_cart
from shop.forms import CartAddProductForm

class ProductList(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

class ProductDetail(DeleteView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        return context
    
class ProductForms(forms.ModelForm):
    short_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']

    def clean_name(self):
        name = self.cleaned_data['name']
        if Product.objects.filter(name=name).exists():
            raise forms.ValidationError('Product with this name already exist')
        return name

class ProductCreate(CreateView):
    model = Product
    form_class = ProductForms
    template_name = 'shop/product/form.html'
    success_url = '/'

# Shopping Cart Views

def cart_detail(request):
    cart = get_cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'shop/cart/detail.html', context)

def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_cart(request)
    quantity = request.POST.get('quantity')
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += int(quantity)
        cart_item.save()
    return redirect('shop:cart-detail')

def cart_remove(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('shop:cart-detail')

def cart_update(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    quantity = request.POST.get('quantity')
    cart_item.quantity = quantity
    cart_item.save()
    return redirect('shop:cart-detail')