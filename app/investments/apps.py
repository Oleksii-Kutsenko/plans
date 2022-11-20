from django.apps import AppConfig
from django.core.signals import request_finished


class PortfoliosConfig(AppConfig):
    """
    Portfolios app config
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "investments"

    def ready(self) -> None:
        from investments import signals

        request_finished.connect(signals.validate_portfolio)
