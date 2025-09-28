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
            # save emptry cart
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart

    def add(self, product, quantity=1):
        """
        Add product to cart or update
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': product.price}
        self.cart[product_id]['quantity'] += quantity
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
