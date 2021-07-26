"""Custom test runner"""
from django.test.runner import DiscoverRunner

from user.management.commands.create_groups import Command


class CustomTestRunner(DiscoverRunner):
    """Custom runner for populating groups"""

    def setup_databases(self, **kwargs):
        """DB setup of test"""
        _return = super().setup_databases(**kwargs)
        Command().handle()
        return _return
