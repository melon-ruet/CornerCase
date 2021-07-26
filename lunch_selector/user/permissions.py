"""All DRF permissions for different level of users"""
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.permissions import DjangoModelPermissions


class AdminPermission(permissions.IsAuthenticated):
    """admin permission checker class"""

    def has_permission(self, request, view):
        """chek admin permission"""
        has_perm = super().has_permission(request, view)
        return has_perm and request.user.user_type == get_user_model().ADMIN


class CustomDjangoModelPermissions(DjangoModelPermissions):
    """Add model view permission"""
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }
