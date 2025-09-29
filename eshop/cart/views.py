from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from shop.models import Product
from .forms import CartAddProductForm
from .cart import Cart

@require_POST
def add_cart(request, product_id):
    """
    Add product to cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product,
                                id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:detail')

@require_POST
def remove_cart(request, product_id):
    """
    Remove product from cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product,
                                id=product_id)
    cart.remove(product)
    return redirect('cart:detail')

def clear_cart(request):
    """
    Clear all from cart
    """
    cart = Cart(request)
    cart.clear()
    return redirect('shop:product_list')

def cart_detail(request):
    """
    Cart's detail
    """
    cart = Cart(request)
    return render(request, 'cart/detail.html',
                  {'cart': cart})