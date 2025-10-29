from django import forms

from .models import Product, Category, Image, Video
from django.core.exceptions import ValidationError
from utils.forms_utils import FormControlMixin

class ProductForm(FormControlMixin, forms.ModelForm):
    """
    Form for edit or update Product model
    set up elements for bootstrap
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'category',
                  'image', 'price', 'available']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['available'].widget.attrs['class'] = 'form-check-input'

class CategoryForm(FormControlMixin, forms.ModelForm):
    """
    Edit category Form
    """
    class Meta:
        model = Category
        fields = ['name']
        
    def clean_name(self):
        """
        Validate name for unique
        """
        name = self.cleaned_data['name']
        print(f"DEBUG: clean_name called with: '{name}'")
        if name:
            queryset = Category.objects.filter(name__iexact=name)
            print(f"DEBUG: Found {queryset.count()} existing categories")
            if self.instance and self.instance.pk:
                print(f"DEBUG: Editing existing instance with pk: {self.instance.pk}")
                queryset = queryset.exclude(pk=self.instance.pk)
            # check unique
            if queryset.exists():
                print("DEBUG: Validation error raised") 
                raise ValidationError('Category with that name '\
                                        'already exists')
        return name


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for inner forms
        self.fields['name'].widget.attrs['id'] = 'id_category_name'

class ImageForm(forms.ModelForm):
    """
    Form for Image model
    """
    class Meta:
        model = Image
        fields = ['content']

class VideoForm(forms.ModelForm):
    """
    Form for video model
    """
    class Meta:
        model = Video
        fields = ['content']