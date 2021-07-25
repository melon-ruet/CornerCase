"""Models for user and user management"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager, Group


class CustomUserManager(UserManager):
    """Custom user manager to set admin type for superuser"""

    @staticmethod
    def _add_to_group(user):
        """Add user to group"""
        group = Group.objects.get_by_natural_key(user.user_type)
        user.groups.add(group)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Override default createsuperuser command"""
        extra_fields.setdefault("user_type", SelectorUser.ADMIN)
        user = super().create_superuser(username, email, password, **extra_fields)
        self._add_to_group(user)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        """Override to add user to group"""
        user = super().create_user(username, email, password, **extra_fields)
        self._add_to_group(user)
        return user


class SelectorUser(AbstractUser):
    """Custom model for additional fields"""
    ADMIN = "admin"
    EMPLOYEE = "employee"
    RESTAURANT_MANAGER = "restaurant_manager"

    USER_TYPES = (
        (ADMIN, _("Admin")),
        (EMPLOYEE, _("Employee")),
        (RESTAURANT_MANAGER, _("Restaurant manager")),
    )
    user_type = models.CharField(verbose_name=_("User Type"), max_length=30, choices=USER_TYPES)

    objects = CustomUserManager()
    REQUIRED_FIELDS = []
