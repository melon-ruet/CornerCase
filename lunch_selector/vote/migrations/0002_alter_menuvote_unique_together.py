# Generated by Django 3.2.5 on 2021-07-26 11:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='menuvote',
            unique_together={('employee', 'day')},
        ),
    ]