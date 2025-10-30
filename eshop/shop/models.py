from unidecode import unidecode
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .fields import OrderField

class SlugByNameMixin:
    """
    Mixin for generating slug by name
    """
    __slug_field_name = 'slug'
    __slug_from_field = 'name'
    
    def __slug_queryset(self, model_class, slug):
        """
        Queryset of slugs
        return queryset
        """
        slug_filter = {self.__slug_field_name: slug}
        queryset = model_class.objects.filter(**slug_filter)
        # exclude current item
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)
        return queryset

    def __generate_unique_slug(self):
        """
        Generate unique slug for each item
        """
        slug_value = unidecode(getattr(self, self.__slug_from_field))
        slug = slugify(slug_value)
        num = 1
        model_class = self.__class__

        # create queryset
        queryset = self.__slug_queryset(model_class, slug)

        while queryset.exists():
            slug = f'{slug}-{num}'
            queryset = self.__slug_queryset(model_class, slug)
            num += 1

        return slug

    def save(self, *args, **kwargs):
        """
        Save item instance
        """
        if self.pk:
            try:
                # if update item
                old_instance = self.__class__.objects.get(pk=self.pk)
                old_value = getattr(old_instance, self.__slug_from_field)
                new_value = getattr(self, self.__slug_from_field)
                if old_value != new_value:
                    setattr(self, self.__slug_field_name,
                            self.__generate_unique_slug())
            except self.__class__.DoesNotExist:
                pass
        elif not getattr(self, self.__slug_field_name):
            setattr(self, self.__slug_field_name,
                    self.__generate_unique_slug())
        super().save(*args, **kwargs)

class Category(SlugByNameMixin, models.Model):
    """
    Product's category model
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

class Product(SlugByNameMixin, models.Model):
    """
    Product model
    if available = False, item not selling
    fields:
        name, slug, description, category, image, price, available
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
    Content for product like images, videos
    Using contenttypes framework and generic foreign key
    to relate content from different tables with product
    """
    product = models.ForeignKey(Product,
                                related_name='content',
                                on_delete=models.CASCADE)
    # For content of description
    # used contenttypes framework
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':(
                                        #  'text',
                                         'image',
                                         'video'
                                     )}
                                     )
    object_id = models.PositiveBigIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    def delete(self, *args, **kwargs):
        """
        Remove related object if exist
        """
        if self.item:
            self.item.delete()
        super().delete(*args, **kwargs)

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
        
class Image(DescriptionBase):
    """
    Image content
    """
    content = models.ImageField(upload_to='products/%Y/%m/%d')

class Video(DescriptionBase):
    """
    Video content
    """
    content = models.URLField()