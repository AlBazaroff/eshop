from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

def create_order(request):
    """
    Create order by cart
    """
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
            messages.success(
                request,
                f'Your order successfully created. Order №{order.id}'
            )
            return redirect('shop:product_list')
    else:
        create_form = OrderCreateForm()
    return render(request,
                  'orders/create_order.html',
                  {'cart': cart,
                   'create_order_form': create_form})