#!admin_views.py
"""
Views for seller functionality in shop
"""
from django.utils import timezone
from django.db.models import Count, Case, When
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST

from easy_thumbnails.files import get_thumbnailer

from .models import Product, Category, ProductContent, Video, Image
from .forms import ProductForm, CategoryForm, VideoForm, ImageForm
from .utils import get_product_content, generate_thumbnail

CONTENT_FORM_MAP = {
    'image': ImageForm,
    'video': VideoForm,
}

@staff_member_required
def admin_product_list(request):
    """
    Admin product list view in the admin panel
    to add, update, remove products on pages
    """
    products = Product.objects.all().order_by('-updated')
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
    # get product with related content(ProductContent)
    try:
        product = Product.objects.prefetch_related('content').\
            get(pk=product_id)
    except Product.DoesNotExist:
        return Http404('Product not found')
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
    # select related content
    image_content = product.content.filter(content_type__model='image')
    video_content = product.content.filter(content_type__model='video')
    # get actual video and image objects
    # prevent N+1 queries
    videos = Video.objects.filter(id__in=video_content.values('object_id'))
    images = Image.objects.filter(id__in=image_content.values('object_id'))

    # build mapping from object id -> ProductContent id
    # so template can use PC id for deletes
    image_pc_map = {pc.object_id: pc.pk for pc in image_content}
    video_pc_map = {pc.object_id: pc.pk for pc in video_content}

    images_with_pc = []
    for it in images:
        images_with_pc.append({'pc_id': image_pc_map.get(it.id), 'item': it})

    videos_with_pc = []
    for it in videos:
        videos_with_pc.append({'pc_id': video_pc_map.get(it.id), 'item': it})

    return render(request,
                  'shop/product/admin/edit_product.html',
                  {'product': product,
                   'form': product_form,
                   'category_form': category_form,
                   'videos': videos_with_pc,
                   'images': images_with_pc})

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
    # get categories with fields: total_products and available_products
    categories = Category.objects.values('id', 'name').\
        annotate(total_products = Count('products__id'),
                 available_products = Count(
                     Case(When(products__available=True, then=1))
                 ))
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
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return JsonResponse({'success': True,
                                 'category_id': category.pk,
                                 'category_name': category.name},
                                 status=201)
        return JsonResponse({"success": False,
                             "error": form.errors['name'].as_text().strip('* ')},
                             status=404)
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"},
                            status=405)

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

@require_POST
@staff_member_required
def product_content_add(request, product_id):
    """
    Add content (image or video) to product
    """
    product = get_object_or_404(Product, pk=product_id)
    content_type = request.POST.get('type')
    FormClass = CONTENT_FORM_MAP.get(content_type)
    if not FormClass:
        return JsonResponse({'error': 'Invalid content type'}, status=400)

    # pass both POST and FILES (images require FILES)
    form = FormClass(request.POST, request.FILES)
    if form.is_valid():
        item = form.save()
        pc = ProductContent.objects.create(
            product=product,
            content_type=ContentType.objects.get_for_model(item),
            object_id=item.id,
        )
        # update related product 'updated' field
        product.updated = timezone.now()
        product.save(update_fields=['updated'])

        # prepare content value (for image return URL if available)
        content_value = None
        try:
            # ImageField has .url
            content_value = item.content.url
        except Exception:
            content_value = getattr(item, 'content', '')

        if content_type == 'image':
            content_value = generate_thumbnail(item)

        return JsonResponse({'success': True,
                             'new_item': {
                                 'id': item.id,
                                 'content': content_value
                                 },
                             'content_id': pc.pk
                             },
                             status=201)
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@require_POST
@staff_member_required
def product_content_delete(request, content_id):
    """
    Delete content (image or video) from product
    """
    content = get_object_or_404(ProductContent, pk=content_id)
    try:
        content.delete()
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': True})