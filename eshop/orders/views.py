from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


def check_cart(func):
    """
    Decorator for checking cart
    before redirect to create_order
    If cart is empty return Http404
    else return create_order
    """
    def wrapper(*args, **kwargs):
        request = args[0]
        cart = Cart(request)
        if cart:
            return func(*args, **kwargs)
        else:
            raise Http404('Your cart is empty. Add products to cart')
    return wrapper
    
@check_cart
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
            request.session['order_id'] = order.id
            # to orders payment
            return redirect('payment:process')
    else:
        create_form = OrderCreateForm(user)
    return render(request,
                  'orders/create_order.html',
                  {'cart': cart,
                   'create_order_form': create_form})