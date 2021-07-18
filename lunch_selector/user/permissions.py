"""All DRF permissions for different level of users"""
from rest_framework import permissions


class SuperuserPermission(permissions.BasePermission):
    """superuser permission checker class"""

    def has_permission(self, request, view):
        """chek superuser permission"""
        return request.user.is_superuser
