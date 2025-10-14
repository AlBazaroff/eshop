# context_processors.py
"""
Add usability for cart in every page
Uses for dynamic counting of cart items in base.html
"""
from .cart import Cart

def cart(request):
    return {'cart': Cart(request)}