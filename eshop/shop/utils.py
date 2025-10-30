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

def generate_thumbnail(image, size=(100, 100), crop=False):
    """
    Generate a thumbnail for a given image
    Args:
        image: Image instance
        size: tuple of (width, height) for the thumbnail
    """
    thumbnailer = get_thumbnailer(image.content)
    thumb_options = {'size': size,
                     'crop': crop}
    thumb = thumbnailer.get_thumbnail(thumb_options)
    return thumb.url

def get_video_thumbnail_url(video):
    """
    Get the thumbnail URL for a video
    Args:
        video: Video instance
    Returns:
        URL string of the video's thumbnail
    """
    url = video.content
    return f'https://img.youtube.com/vi/{url.split('/')[-1]}/0.jpg'