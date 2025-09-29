from django.shortcuts import render

from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        create_form = OrderCreateForm(request.POST)
        if create_form.is_valid():
            order = create_form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request,
                          'orders/create_order.html',
                          {'order': order})
    else:
        create_form = OrderCreateForm()
    return render(request,
                  'orders/create_order.html',
                  {'cart': cart,
                   'create_order_form': create_form})