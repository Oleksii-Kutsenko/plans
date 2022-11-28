"""
Investments app settings
"""
from django.apps import AppConfig


class PortfoliosConfig(AppConfig):
    """
    Portfolios app config
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "investments"

    def ready(self) -> None:
        pass
