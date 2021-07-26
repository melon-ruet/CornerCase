"""Configs for vote app"""
from django.apps import AppConfig


class VoteConfig(AppConfig):
    """Vote app config class"""
    default_auto_field = "django.db.models.BigAutoField"
    name = "vote"
