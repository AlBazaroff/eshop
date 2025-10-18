from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Order, OrderItem

def stripe_payment(obj):
    """
    Field for list_display in admin panel
    return html code
    """
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''

# description for field
stripe_payment.short_description = 'Stripe payment'

class OrderItemInline(admin.TabularInline):
    """
    Inline part of order
    contain products from order
    """
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Handle orders in admin panel
    """
    list_display = ['first_name', 'last_name', 'email',
                    'city', 'address', 'postal_code',
                    stripe_payment, 'paid', 'created', 'updated' ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
