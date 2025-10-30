from django.shortcuts import render, redirect
from django.contrib import messages

from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from account.models import Profile
from cart.cart import Cart
from cart.decorators import check_cart

    
@check_cart
def create_order(request):
    """
    Create order by cart from session
    """
    cart = Cart(request)
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
    else:
        profile = None

    if request.method == 'POST':
        create_form = OrderCreateForm(user, profile, request.POST)
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
        create_form = OrderCreateForm(user, profile)
    return render(request,
                  'orders/create_order.html',
                  {'cart': cart,
                   'create_order_form': create_form})