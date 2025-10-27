#!admin_views.py
"""
Views for seller functionality in shop
"""
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from .models import Product, Category
from .forms import ProductForm, CategoryForm

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
    category_form = CategoryForm()
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request,
                            f'You successfully updated product №\
                            {product.pk}')
            return redirect('shop:admin_product_list')
    else:
        product_form = ProductForm(instance=product)
    return render(request,
                  'shop/product/admin/edit_product.html',
                  {'product': product,
                   'form': product_form,
                   'category_form': category_form})

@staff_member_required
def product_add(request):
    """
    View for adding new product, works only for admin with permission
    """
    category_form = CategoryForm()
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save()
            messages.success(request,
                             f'You successfully added product №\
                             {product.pk}')
            return redirect('shop:admin_product_list')
    else:
        product_form = ProductForm()
    return render(request,
                  'shop/product/admin/edit_product.html',
                  {'form': product_form,
                   'category_form': category_form})

@staff_member_required
def product_delete(request, product_id):
    """
    View for removing item from webserver
    """
    product = get_object_or_404(Product,
                                pk=product_id)
    try:
        product.delete()
    except Exception as e:
        return Http404()
    return redirect('shop:admin_product_list')

@staff_member_required
def admin_category_list(request):
    """
    View for listing categories in admin panel
    """
    categories = Category.objects.all()
    paginator = Paginator(categories, 30)
    page_num = request.GET.get('page')
    categories = paginator.get_page(page_num)
    return render(request,
                  'shop/product/admin/category_list.html',
                  {'categories': categories})

@require_POST
@staff_member_required
def category_add(request):
    """
    Add new category
    """
    name = request.POST.get('name', '').strip()
    if not name:
        return JsonResponse({'success': False,
                             'error': 'Category name is required'})
    try:
        # Check if category already exist
        if Category.objects.filter(name=name).exists():
            return JsonResponse({'success': False,
                                 'error': 'Category name already exists'},
                                 status=409)
        category = Category.objects.create(name=name)
        return JsonResponse({'success': True,
                             'category_id': category.pk,
                             'category_name': category.name},
                             status=201)
    except Exception as e:
        return JsonResponse({'success': False,
                             'error': str(e)},
                             status=400)

@staff_member_required
def category_update(request, category_id):
    """
    Update category
    """
    category = get_object_or_404(Category, pk=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            return JsonResponse({
                "success": True,
                "category_id": category.id,
                "category_name": category.name,
                },
                status=200)
        return JsonResponse({"success": False,
                             "error": form.errors['name'].as_text().strip('* ')},
                            status=404)
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"},
                            status=405)
    
@staff_member_required
def category_delete(request, category_id):
    """
    Delete category
    """
    category = get_object_or_404(Category, pk=category_id)
    try:
        category.delete()
    except Exception as e:
        return Http404(e)
    return redirect('shop:admin_category_list')