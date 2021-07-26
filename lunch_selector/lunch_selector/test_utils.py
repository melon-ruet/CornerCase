"""Custom test runner"""
from django.contrib.auth import get_user_model
from django.test.runner import DiscoverRunner
from rest_framework.test import APITestCase

from user.management.commands.create_groups import Command


class CustomTestRunner(DiscoverRunner):
    """Custom runner for populating groups"""

    def setup_databases(self, **kwargs):
        """DB setup of test"""
        _return = super().setup_databases(**kwargs)
        Command().handle()
        return _return


class CustomAPITestCase(APITestCase):
    """Custom class for creating token for necessary users"""

    def setUp(self):
        """Override before all of test class"""
        super().setUpClass()
        from rest_framework.authtoken.models import Token
        user_model = get_user_model()

        self.admin_instance = user_model.objects.create_user(
            username="admin",
            user_type=user_model.ADMIN
        )
        self.admin_token, _ = Token.objects.get_or_create(user=self.admin_instance)

        self.manager_instance = user_model.objects.create_user(
            username="manager",
            user_type=user_model.RESTAURANT_MANAGER
        )
        self.manager_token, _ = Token.objects.get_or_create(user=self.manager_instance)

        self.employee_instance = user_model.objects.create_user(
            username="employee",
            user_type=user_model.EMPLOYEE
        )
        self.employee_token, _ = Token.objects.get_or_create(user=self.employee_instance)
