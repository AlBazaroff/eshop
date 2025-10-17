from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Category(models.Model):
    """
    Product's categories
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

class Product(models.Model):
    """
    Product selling in the shop
    if available = False, not selling
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)

    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']), # for search and sorting
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
    
class ProductContent(models.Model):
    """
    Content for product,
    like images, videos
    """
    product = models.ForeignKey(Product,
                                related_name='content',
                                on_delete=models.CASCADE)
    # For content of description
    # used contenttypes framework
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':(
                                         'text',
                                         'image',
                                         'video'
                                     )}
                                     )
    object_id = models.PositiveBigIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

# Models for content based on DescriptionBase 
# return after create admin page for products
class DescriptionBase(models.Model):
    """
    Abstract class for any content
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class Text(DescriptionBase):
    """
    Text content
    """
    content = models.TextField()

class Image(DescriptionBase):
    " Image content "
    file = models.ImageField(upload_to='products/%Y/%m/%d')

class Video(DescriptionBase):
    " Video content "
    file = models.FileField(upload_to='files/')