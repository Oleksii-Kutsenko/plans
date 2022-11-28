"""
Investments schema
"""
import graphene
import numpy
from django.contrib.auth import get_user_model
from django.db.models import Max, Min
from graphene import String

from .graphql_types import PortfolioType
from .models import Portfolio

User = get_user_model()
AGE_OF_MAJORITY = 18


def get_personal_max_drawdown(user):
    """
    Returns personal maximum portfolio drawdown
    Args:
        user:

    Returns:

    """
    min_age = AGE_OF_MAJORITY
    max_age = user.get_pension_age()
    max_drawdown = Portfolio.objects.aggregate(Min("max_drawdown"))["max_drawdown__min"]
    min_drawdown = Portfolio.objects.aggregate(Max("max_drawdown"))["max_drawdown__max"]
    result = numpy.polyfit([min_age, max_age], [max_drawdown, min_drawdown], 2)

    user_age = user.get_age()
    personal_max_drawdown = round(
        result[0] * user_age**2 + result[1] * user_age + result[2], 4
    )

    if personal_max_drawdown < max_drawdown:
        personal_max_drawdown = max_drawdown
    elif personal_max_drawdown > min_drawdown:
        personal_max_drawdown = min_drawdown

    return personal_max_drawdown


class QueryPortfolios(graphene.ObjectType):
    """
    Portfolios query
    """

    best_portfolios_by_performance = graphene.List(
        PortfolioType, username=String(required=False)
    )

    def resolve_best_portfolios_by_performance(self, info, username=None):
        """
        Return the best matching portfolios sorted by annualized return
        Args:
            info: Graphene info
            username: Optional username

        Returns:
            List[PortfolioType]: List of portfolios
        """
        user = info.context.user
        if username:
            user = User.objects.get(username=username)
        personal_max_drawdown = get_personal_max_drawdown(user)
        portfolios = Portfolio.objects.filter(
            max_drawdown__gte=personal_max_drawdown
        ).order_by("-cagr")[:10]
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
    def mutate(cls, root, info, portfolio_id, visible):
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


schema = graphene.Schema(query=QueryPortfolios, mutation=UpdatePortfolio)
