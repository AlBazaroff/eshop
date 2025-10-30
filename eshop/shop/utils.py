from django.contrib.contenttypes.models import ContentType
from easy_thumbnails.files import get_thumbnailer

def get_product_content(product, model):
    """
    get related content of specific type for a product
    Args:
        product: Product instance
        model: content model name as string ('image' or 'video')
    Returns:
        QuerySet of ProductContent filtered by content type
    """
     # select related content
    content = product.content.filter(content_type = ContentType.\
                                     objects.get_for_model(model))
    # prevent N+1 queries
    items = model.objects.filter(id__in=content.values('object_id'))
    return items

def generate_thumbnail(image, size=(100, 100)):
    """
    Generate a thumbnail for a given image
    Args:
        image: Image instance
        size: tuple of (width, height) for the thumbnail
    """
    thumbnailer = get_thumbnailer(image.content)
    thumb_options = {'size': size}
    thumb = thumbnailer.get_thumbnail(thumb_options)
    return thumb.url