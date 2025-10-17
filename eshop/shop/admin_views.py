#!admin_views.py
"""
Views for seller functionality in shop
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib import messages

from .models import Product
from .forms import ProductForm

def admin_required(function):
    """
    Decorator checking for admin permission
    """
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            return function(*args, **kwargs)
        else:
            raise Http404()
    return wrapper

@login_required
@admin_required
def admin_product_list(request):
    """
    product list for admin
    """
    products = Product.objects.all()
    paginator = Paginator(products, 30)
    page_num = request.GET.get('page')
    products = paginator.get_page(page_num)

    return render(request,
                  'shop/product/admin/product_list.html',
                  {'products': products})

@login_required
@admin_required
def admin_product_update(request, product_id):
    """
    Update existing products by admin
    """
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request,
                            f'You successfully updated product №\
                            {product.pk}')
            return redirect('shop:admin_product_list')
    else:
        form = ProductForm()
    return render(request,
                  'shop/product/admin/edit_product.html',
                  {'product': product,
                   'form': form})

@login_required
@admin_required
def admin_product_add(request):
    """
    Add new product
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request,
                             f'You successfully update product №\
                             {product.pk}')
            return redirect('shop:admin_product_list')
    else:
        form = ProductForm
    return render(request,
                  'shop/product/admin/edit_product.html',
                  {'form': form})
