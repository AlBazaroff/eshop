from django.db import models
from django.core.validators import RegexValidator

from shop.models import Product
from account.models import User

class Order(models.Model):
    """
    Serve for users orders
    """
    # if user authenticated create order
    # we define him
    user = models.ForeignKey(User,
                             related_name='orders',
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True)
    # replace first_name, last_name, email
    # after adding auth
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    # phone with validator
    # instead, can use django-phonenumber-field
    phone = models.CharField(
        max_length=17,
        blank=True,
        validators=[
            RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be in format: '+999999999'.\
                Up to 15 digits allowed."
            )
        ],
        verbose_name='Phone Number'
    )

    city = models.CharField(max_length=30)
    address = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=10)

    paid = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['email']),
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