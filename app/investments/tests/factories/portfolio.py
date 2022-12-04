"""
Factories for the Portfolio model and related models
"""
import random

import factory

from investments.models import Portfolio, PortfolioTicker, PortfolioBacktestData
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


class PortfolioBacktestDataFactory(factory.django.DjangoModelFactory):
    """
    PortfolioBacktestData factory
    """

    class Meta:
        """
        Meta class
        """

        model = PortfolioBacktestData

    portfolio = factory.SubFactory(PortfolioFactory)
    max_drawdown = factory.LazyFunction(lambda: random.uniform(-0.99, -0.01))
    cagr = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    standard_deviation = factory.Faker(
        "pyfloat", left_digits=2, right_digits=2, positive=True
    )
    sharpe = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    sortino = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    market_correlation = factory.Faker(
        "pyfloat", left_digits=2, right_digits=2, positive=True
    )
    start_date = factory.Faker("date")
