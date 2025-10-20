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