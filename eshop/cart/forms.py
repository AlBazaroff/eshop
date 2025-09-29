from django import forms

PRODUCT_QUANTITIES = [(i, str(i)) for i in range(1,11)]

class CartAddProductForm(forms.Form):
    """
    Adding product to cart form
    """
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITIES,
                                     coerce=int,
                                     )
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)