from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Category, Product
from cart.forms import CartAddProductForm
from .admin_views import product_update, admin_product_list, product_add,\
    product_delete, category_add, category_update, admin_category_list,\
    category_delete, product_content_add, product_content_delete

def product_list(request, category_slug=None):
    """
    View products on page
    if category_slug define,
    show products in selected category
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        # get products from selected category
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)

    # pagination pages
    paginator = Paginator(products, 7)
    page_number = request.GET.get('page')
    # get products from page
    products = paginator.get_page(page_number)
    
    return render(request,
                  'shop/product/product_list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    """
    View for product's details
    Display details of current product
    Args:
        id: product id
        slug: product slug
    """
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_form = CartAddProductForm()
    return render(request,
                  'shop/product/product_detail.html',
                  {'product': product,
                   'cart_form': cart_form})

def product_search(request, name):
    """
    View for searching Product from catalog by name
    Args:
        name: name of product
    """
    products = Product.objects.filter(name__contains=name)
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    return render(request,
                  'shop/product/product_search.html',
                  {'name': name,
                   'products': products})