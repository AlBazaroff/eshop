from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from shop.models import Product
from .forms import CartAddProductForm
from .cart import Cart

@require_POST
def add_cart(request, product_id):
    """
    Add or change amount items in cart
    Args:
        request: HTTP-request
        product_id: id of product
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
    Remove item from cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product,
                                id=product_id)
    cart.remove(product)
    return redirect('cart:detail')

@require_POST
def clear_cart(request):
    """
    Clear cart from all items
    """
    cart = Cart(request)
    cart.clear()
    return redirect('shop:product_list')

def cart_detail(request):
    """
    Cart's detail
    For every item add form for update
    """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'cart/detail.html',
                  {'cart': cart})