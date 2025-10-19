#!admin_views.py
"""
Views for seller functionality in shop
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from .models import Product
from .forms import ProductForm

@staff_member_required
def admin_product_list(request):
    """
    Admin product list view in the admin panel
    to add, update, remove products on pages
    """
    products = Product.objects.all()
    paginator = Paginator(products, 30)
    page_num = request.GET.get('page')
    products = paginator.get_page(page_num)
    return render(request,
                  'shop/product/admin/product_list.html',
                  {'products': products})

@staff_member_required
def product_update(request, product_id):
    """
    View for updating existing item by admin
    Args:
        product_id: product_id of product for updating
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

@staff_member_required
def product_add(request):
    """
    View for adding new product, works only for admin with permission
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

@staff_member_required
def product_remove(request, product_id):
    """
    View for removing item from webserver
    """
    product = get_object_or_404(Product,
                                pk=product_id)
    product.delete()
    return redirect('shop:admin_product_list')