"""
Factories for the Portfolio model and related models
"""
import factory

from investments.models import Portfolio, PortfolioTicker
from investments.tests.factories.ticker import TickerFactory


class PortfolioFactory(factory.django.DjangoModelFactory):
    """
    Portfolio factory
    """

    class Meta:
        """
        Meta class
        """

        model = Portfolio

    name = factory.Sequence(lambda n: f"Portfolio {n}")


class PortfolioTickerFactory(factory.django.DjangoModelFactory):
    """
    PortfolioTicker factory
    """

    class Meta:
        """
        Meta class
        """

        model = PortfolioTicker

    portfolio = factory.SubFactory(PortfolioFactory)
    ticker = factory.SubFactory(TickerFactory)
    weight = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
