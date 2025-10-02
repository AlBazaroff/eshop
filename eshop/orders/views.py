from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

def create_order(request):
    """
    Create order by cart
    """
    cart = Cart(request)
    user = request.user
    if request.method == 'POST':
        create_form = OrderCreateForm(user, request.POST)
        if create_form.is_valid():
            order = create_form.save(commit=False)
            if request.user.is_authenticated:
                order.user = user
            order.save()
            
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
            # send mail
            order_created.delay(order.id)
            return redirect('shop:product_list')
    else:
        create_form = OrderCreateForm(user)
    return render(request,
                  'orders/create_order.html',
                  {'cart': cart,
                   'create_order_form': create_form})