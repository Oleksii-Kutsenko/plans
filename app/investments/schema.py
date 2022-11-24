"""
Investments schema
"""
import graphene
import numpy
from django.contrib.auth import get_user_model
from django.db.models import Max, Min
from graphene import String
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug

from .models import Portfolio

User = get_user_model()
AGE_OF_MAJORITY = 18


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
        )


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
    personal_max_drawdown = result[0] * user_age**2 + result[1] * user_age + result[2]
    return personal_max_drawdown


class PortfoliosQuery(graphene.ObjectType):
    """
    Portfolios query
    """

    best_portfolios_by_performance = graphene.List(
        PortfolioType, username=String(required=False)
    )
    debug = graphene.Field(DjangoDebug, name="_debug")

    def resolve_best_portfolios_by_performance(self, info, username=None):
        """
        Return the best matching portfolios sorted by annualized return
        Args:
            info: Graphene info
            username: Optonal username

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


schema = graphene.Schema(query=PortfoliosQuery)
