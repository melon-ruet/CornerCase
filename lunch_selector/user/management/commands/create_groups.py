from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from user.models import SelectorUser


class Command(BaseCommand):
    help = "Create or update user groups"

    def handle(self, *args, **options):
        groups = {
            SelectorUser.ADMIN: Permission.objects.values_list("codename", flat=True),
            SelectorUser.RESTAURANT_MANAGER: {
                "add_restaurant",
                "change_restaurant",
                "delete_restaurant",
                "view_restaurant",
                "add_menu",
                "change_menu",
                "delete_menu",
                "view_menu",
            },
            SelectorUser.EMPLOYEE: {
                "view_menu",
                "view_menuvote",
                "add_menuvote",
                "delete_menuvote",
                "change_menuvote",
            }
        }

        for name, permissions in groups.items():
            permissions = Permission.objects.filter(
                codename__in=permissions
            )
            group, _ = Group.objects.update_or_create(
                **{"name": name}
            )
            group.permissions.add(*permissions)

            self.stdout.write(
                self.style.SUCCESS(f"Successfully created/updated groups {name}")
            )
