from typing import Any, Optional

from django.db.models.signals import pre_save
from django.dispatch import receiver

from investments.models import Portfolio, PortfolioTicker


@receiver(pre_save, sender=Portfolio)
def validate_portfolio(
    sender: Any, instance: Optional[Portfolio] = None, **kwargs: dict
) -> None:
    """
    Validates portfolio before saving
    """
    if instance:
        portfolio_tickers = PortfolioTicker.objects.filter(portfolio=instance.id)
        if portfolio_tickers.exists():
            assert (
                round(sum(portfolio_tickers.values_list("weight", flat=True)), 4)
                == 100.0
            )
