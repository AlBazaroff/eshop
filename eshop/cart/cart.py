#!cart.py
"""
Implementation of cart in app
"""

from decimal import Decimal
from django.conf import settings

from shop.models import Product

class Cart:
    def __init__(self, request):
        """
        Initialize cart for new session
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # save empty cart
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
        self._products = None

    def _get_products(self):
        """
        Cache products for preventing double query
        """
        if self._products is None:
            product_ids = self.cart.keys()
            self._products = Product.objects.filter(id__in=product_ids)
        return self._products

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add or update items in cart
        Args:
            product: instance of product model
            quantity: amount of item
            override_quantity: override quantity of existing item in cart
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        # if in the cart we change item's quantity
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        # if price was changed
        if self.cart[product_id]['price'] != str(product.price):
            self.cart[product_id]['price'] = str(product.price)

        # reset cache before save
        self._products = None
        self.save()

    def save(self):
        """
        save session to update cart
        """
        # mark session as changed
        self.session.modified = True

    def remove(self, product):
        """
        Remove item from cart
        """
        product_id = str(product.id)
        if self.cart[product_id]:
            del self.cart[product_id]
            # reset cache
            self._products = None
            self.save()

    def clear(self):
        """
        Clear cart
        by session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def total_price(self):
        """
        Calculate total price of all items in cart
        Calc: price * quantity
        """
        return sum(Decimal(value['price']) * value['quantity']
            for value in self.cart.values())

    def __iter__(self):
        """
        Iteration of items in cart
        create temp_cart
        add product to temp_cart for every item
        """
        products = self._get_products()
        # save product in temp_cart
        temp_cart = self.cart.copy()
        for product in products:
            temp_cart[str(product.id)]['product'] = product

        for item in temp_cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def __len__(self):
        """
        return total count of products in the cart 
        """
        return sum(item['quantity']
                   for item in self.cart.values())