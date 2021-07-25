from django.test.runner import DiscoverRunner

from user.management.commands.create_groups import Command


class CustomTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        _return = super().setup_databases(**kwargs)
        Command().handle()
        return _return
