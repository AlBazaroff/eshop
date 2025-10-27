from django import forms

from .models import Product, Category
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for inner forms
        self.fields['name'].widget.attrs['id'] = 'id_category_name'