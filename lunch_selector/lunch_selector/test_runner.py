from django.test.runner import DiscoverRunner


class CustomTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        _return = super().setup_databases(**kwargs)
        from user.management.commands.create_groups import Command
        Command().handle()
        return _return
