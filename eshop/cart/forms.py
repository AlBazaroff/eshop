from django.forms import forms

PRODUCT_QUANTITIES = [(i, str(i)) for i in range(1,11)]

class CartAddProduct(forms.Form):
    """
    Adding product to cart form
    """
    quantity = forms.TypeChoiceField(choice=1,
                                     coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)