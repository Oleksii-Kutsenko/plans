"""
Investments schema
"""
from typing import Optional

import graphene
import numpy
from django.db.models import Max, Min
from graphene import String, Int
from graphql import GraphQLResolveInfo

from accounts.models import User
from .graphql_types import PortfolioType
from .models import Portfolio, PortfolioBacktestData


def get_personal_max_drawdown(user: User, age: Optional[int] = None) -> float:
    """
    Returns personal maximum portfolio drawdown
    Args:
        user: User object
        age: Custom age for calculation
    Returns:
        Maximum portfolio drawdown
    """
    if PortfolioBacktestData.objects.count() <= 2:
        raise ValueError("Not enough backtest data for calculation")

    min_age = 1
    max_age = user.get_pension_age()
    max_drawdown = PortfolioBacktestData.objects.aggregate(Min("max_drawdown"))[
        "max_drawdown__min"
    ]
    min_drawdown = PortfolioBacktestData.objects.aggregate(Max("max_drawdown"))[
        "max_drawdown__max"
    ]
    result = numpy.polyfit([min_age, max_age], [max_drawdown, min_drawdown], 1)

    user_age = age if age else user.get_age()
    personal_max_drawdown = result[0] * user_age + result[1]

    if personal_max_drawdown < max_drawdown:
        personal_max_drawdown = max_drawdown
    elif personal_max_drawdown > min_drawdown:
        personal_max_drawdown = min_drawdown

    return personal_max_drawdown


class PortfoliosQuery(graphene.ObjectType):
    """
    Portfolios query
    """

    best_portfolios_by_performance = graphene.List(
        PortfolioType,
        age=Int(required=False),
        username=String(required=False),
    )

    def resolve_best_portfolios_by_performance(
        self: Optional[graphene.ObjectType],
        info: GraphQLResolveInfo,
        age: Optional[int] = None,
        username: Optional[str] = None,
    ) -> list[Portfolio]:
        """
        Return the best matching portfolios sorted by annualized return
        Args:
            info: Graphene info
            age: Custom age to use for portfolio selection
            username: Optional username

        Returns:
            List[PortfolioType]: List of portfolios
        """
        user = info.context.user
        if username:
            user = User.objects.get(username=username)
        personal_max_drawdown = get_personal_max_drawdown(user, age)
        portfolios = (
            Portfolio.objects.filter(
                backtest_data__max_drawdown__gte=personal_max_drawdown
            )
            .order_by("-backtest_data__cagr")
            .select_related()[:10]
        )
        return portfolios


class PortfolioMutation(graphene.Mutation):
    """
    Portfolio mutation
    """

    class Arguments:
        """
        Arguments
        """

        portfolio_id = graphene.ID()
        visible = graphene.Boolean()

    portfolio = graphene.Field(PortfolioType)

    @classmethod
    def mutate(
        cls,
        root: Optional[graphene.Mutation],
        info: GraphQLResolveInfo,
        portfolio_id: str,
        visible: bool,
    ) -> "PortfolioMutation":
        """
        Updates portfolio visibility
        Args:
            root: Graphene root
            info: Graphene info
            portfolio_id: Portfolio id
            visible: Portfolio visibility

        Returns:
            PortfolioMutation: Portfolio mutation
        """
        portfolio = Portfolio.objects.get(pk=portfolio_id)
        portfolio.visible = visible
        portfolio.save()
        return cls(portfolio=portfolio)


class UpdatePortfolio(graphene.ObjectType):
    """
    Portfolios mutation
    """

    update_portfolio = PortfolioMutation.Field()
