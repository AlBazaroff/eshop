#!backends.py
"""
backend for account
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import get_object_or_404

class EmailBackend(ModelBackend):
    """
    Authenticate user by email
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        " authenticate user "
        UserModel = get_user_model()
        user = get_object_or_404(UserModel,
                                 email=username)
        if user.check_password(password):
            return user
        return None