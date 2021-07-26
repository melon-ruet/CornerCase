"""Voting related models"""
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from restaurant.models import Menu
from user.models import SelectorUser


class MenuVote(models.Model):
    """Vote each menu per day"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_menu = self.menu

    menu = models.ForeignKey(
        to=Menu, verbose_name=_("menu"),
        on_delete=models.CASCADE, related_name="votes"
    )
    employee = models.ForeignKey(
        to=SelectorUser, verbose_name=_("name"),
        on_delete=models.CASCADE, related_name="votes"
    )
    day = models.DateField(verbose_name=_("date"), default=datetime.date.today)

    def __str__(self):
        return f"{self.menu.name}-{self.day}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """update vote_count in menu"""
        if self.pk:
            if self.old_menu != self.menu:
                self.old_menu.vote_count = self.old_menu.vote_count - 1
                self.old_menu.save()
                self.menu.vote_count = self.menu.vote_count + 1
                self.menu.save()
        else:
            self.menu.vote_count = self.menu.vote_count + 1
            self.menu.save()

        super().save(force_insert, force_update, using, update_fields)

    class Meta:  # pylint: disable=missing-class-docstring
        unique_together = ("employee", "day")
