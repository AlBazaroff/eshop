#! user_orders.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from orders.models import Order, OrderItem

@login_required
def order_list(request):
    """
    Check orders placed by current user
    """
    orders = Order.objects.filter(user=request.user)
    return render(request,
                  'account/orders/order_list.html',
                  {'orders': orders})

@login_required
def order_detail(request, order_id):
    """
    Check order detail
    """
    order = get_object_or_404(Order,
                              pk=order_id,
                              user=request.user)
    # add to items joins for product, to prevent N+1
    items = OrderItem.objects.filter(order=order).select_related('product')

    total_cost = sum([item.get_cost() for item in items])

    return render(request,
                  'account/orders/order_detail.html',
                  {'total_cost': total_cost,
                   'order': order,
                   'items': items})