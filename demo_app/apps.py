"""
Django app configuration for the demo app
"""

from django.apps import AppConfig


class DemoAppConfig(AppConfig):
    """
    Configuration for the demo app
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "demo_app"
    verbose_name = "Demo Application"
