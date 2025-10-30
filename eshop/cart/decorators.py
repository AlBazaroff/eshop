#!decorators.py
"""
Decorators for cart
"""
from django.http import Http404
from .cart import Cart

def check_cart(view):
    """
    Decorator for checking cart
    before redirect to create_order
    If cart is empty return Http404
    else return create_order
    """
    def wrapper(request, *args, **kwargs):
        cart = Cart(request)
        if cart:
            return view(request, *args, **kwargs)
        else:
            raise Http404('Your cart is empty. Add products to cart')
    return wrapper