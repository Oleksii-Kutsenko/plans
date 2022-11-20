"""
Ticker factory
"""
import factory

from ...models import Ticker


class TickerFactory(factory.django.DjangoModelFactory):
    """
    Ticker factory
    """
    class Meta:
        """
        Meta class
        """
        model = Ticker

    name = factory.Sequence(lambda n: f"Ticker {n}")
    symbol = factory.Sequence(lambda n: f"TICKER{n}")
