"""Model related to restaurant and menu"""
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from user.models import SelectorUser


class Restaurant(models.Model):
    """
    Assuming a restaurant have only one manager and
    a manager can have multiple restaurants
    """
    name = models.CharField(verbose_name=_("name"), unique=True, max_length=100)
    manager = models.ForeignKey(
        to=SelectorUser, verbose_name=_("manager"),
        on_delete=models.CASCADE
    )

    def clean(self):
        """Check if user type is manager"""
        if self.manager.user_type != SelectorUser.RESTAURANT_MANAGER:
            raise ValidationError({"manager": _("user_type must be restaurant manager")})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """Django default save model override"""
        self.clean()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name
