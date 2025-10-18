from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile

@admin.register(User)
class UserAdmin(UserAdmin):
    """
    Custom UserAdmin for model User
    email is main field instead username
    """
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    
    ordering = ['email']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    User profiles in admin panel
    """
    list_display = ['user', 'phone', 'city', 'postal_code']
    list_filter = ['city']
    raw_id_fields = ['user']