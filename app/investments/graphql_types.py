"""
GraphQL types from investments models
"""
from graphene_django import DjangoObjectType

from investments.models import Portfolio


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
            "cagr",
            "standard_deviation",
            "sharpe",
            "sortino",
            "market_correlation",
            "max_drawdown",
            "visible",
        )
