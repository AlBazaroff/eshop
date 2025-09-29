from django.db import models

from shop.models import Product

class Order(models.Model):
    """
    Serve for users orders
    """
    # replace first_name, last_name, email
    # after adding auth
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    city = models.CharField(max_length=30)
    address = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=10)

    paid = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        " return total cost of order "
        return sum(item.get_cost()
                   for item in self.items.all())

class OrderItem(models.Model):
    """
    Content order items
    """
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return (self.id)
    
    def get_cost(self):
        " return cost of items in the position "
        return (self.price * self.quantity)