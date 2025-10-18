import stripe

from decimal import Decimal

from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from orders.models import Order, OrderItem

# stripe keys from settings
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def annulment(request):
    """
    Cancel payment before payment
    initiate by cancel on the page
    remove order_id from session
    """
    del request.session['order_id']
    return redirect('shop:product_list')

def payment_canceled(request):
    """
    Work if stripe payment was canceled
    remove order_id from session
    """
    del request.session['order_id']
    return render(request, 'payment/canceled.html')

def payment_completed(request):
    """
    Work if stripe payment was successfully completed
    """
    order_id = request.session['order_id']
    order = Order.objects.get(id=order_id)
    order.paid = True
    order.save()
    del request.session['order_id']
    return render(request, 'payment/completed.html')

# the page is not cached
@never_cache
def payment_process(request):
    """
    Start process of payment on stripe pages
    Started after order creation was successful
    use order data by order_id from current session
    """
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order,
                              id=order_id)
    order_items = OrderItem.objects.filter(order=order).select_related('product')
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        # data for Stripe checkout session
        data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': [],
        }
        # add dynamic items
        # by data stored in the db
        for item in order.items.all():
            data['line_items'].append({
                'price_data':{
                    'unit_amount':int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data':{
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })
        # create Checkout session
        session = stripe.checkout.Session.create(**data)
        
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', {
            'order': order,
            'order_items': order_items,
        })