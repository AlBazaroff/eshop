from django import forms

from .models import Product
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