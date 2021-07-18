"""Models for user and user management"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser


class SelectorUser(AbstractUser):
    """Custom model for additional fields"""
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"
    RESTAURANT_MANAGER = "RESTAURANT_MANAGER"

    USER_TYPES = (
        (ADMIN, _("Admin")),
        (EMPLOYEE, _("Employee")),
        (RESTAURANT_MANAGER, _("Restaurant manager")),
    )
    user_type = models.CharField(verbose_name=_("User Type"), choices=USER_TYPES)
