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

    @classmethod
    def setUpClass(cls):
        """Override before all of test class"""
        super().setUpClass()
        from rest_framework.authtoken.models import Token
        user_model = get_user_model()

        cls.admin_instance = user_model.objects.create_user(
            username="admin",
            user_type=user_model.ADMIN
        )
        cls.admin_token, _ = Token.objects.get_or_create(user=cls.admin_instance)

        cls.manager_instance = user_model.objects.create_user(
            username="manager",
            user_type=user_model.RESTAURANT_MANAGER
        )
        cls.manager_token, _ = Token.objects.get_or_create(user=cls.manager_instance)

        cls.employee_instance = user_model.objects.create_user(
            username="employee",
            user_type=user_model.EMPLOYEE
        )
        cls.employee_token, _ = Token.objects.get_or_create(user=cls.employee_instance)
