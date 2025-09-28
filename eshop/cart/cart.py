from decimal import Decimal
from django.conf import settings

from shop.models import Product

class Cart:
    def __init__(self, request):
        """
        Initialize cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # save empty cart
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add product to cart or update
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': product.price}
        # if in the cart we change item's quantity
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        # if price was changed
        if self.cart[product_id]['price'] != product.price:
            self.cart[product_id]['price'] = product.price
        self.save()

    def save(self):
        # mark session like changed
        self.session.modified = True

    def remove(self, product):
        """
        remove from cart
        """
        product_id = str(product.id)
        if self.cart[product_id]:
            del self.cart[product_id]
            self.save()

    def clear(self):
        " clear cart "
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def total_price(self):
        return sum(Decimal(value['price']) * value['quantity']
            for value in self.cart.values())

    def __iter__(self):
        """
        iter for items in cart 
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        # save temp product in cart
        temp_cart = self.cart.copy()
        for product in products:
            temp_cart[str(product.id)][product] = product

        for item in temp_cart.values:
            item['price'] = Decimal(item['price'])
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def __len__(self):
        """
        return total count of products
        in the cart 
        """
        return sum(item['quantity']
                   for item in self.cart.value())