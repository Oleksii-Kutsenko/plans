"""
GraphQL types from investments models
"""
from graphene_django import DjangoObjectType

from investments.models import Portfolio, PortfolioBacktestData


class PortfolioType(DjangoObjectType):
    """
    Portfolio type
    """

    class Meta:
        """
        Meta
        """

        model = Portfolio
        fields = (
            "name",
            "visible",
            "backtest_data",
        )


class PortfolioBacktestDataType(DjangoObjectType):
    """
    PortfolioBacktestData type
    """

    class Meta:
        """
        Meta
        """

        model = PortfolioBacktestData
        fields = (
            "cagr",
            "max_drawdown",
            "sharpe",
            "standard_deviation",
            "start_date",
        )
