from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Category, Product
from cart.forms import CartAddProductForm

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
    View product's details
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