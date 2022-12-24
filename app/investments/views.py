from datetime import date
from typing import Optional

import numpy
from django.db.models import Min, Max
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.models import User
from investments.models import Portfolio, PortfolioBacktestData
from investments.serializers import PortfolioSerializer


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
    if max_age is None:
        raise ValueError("User has no pension age")
    max_drawdown = PortfolioBacktestData.objects.aggregate(Min("max_drawdown"))[
        "max_drawdown__min"
    ]
    min_drawdown = PortfolioBacktestData.objects.aggregate(Max("max_drawdown"))[
        "max_drawdown__max"
    ]
    result = numpy.polyfit([min_age, max_age], [max_drawdown, min_drawdown], 1)

    user_age = age if age else user.get_age()
    personal_max_drawdown: float = result[0] * user_age + result[1]

    if personal_max_drawdown < max_drawdown:
        personal_max_drawdown = max_drawdown
    elif personal_max_drawdown > min_drawdown:
        personal_max_drawdown = min_drawdown

    return personal_max_drawdown


class PortfolioViewSet(viewsets.ModelViewSet):
    """
    Portfolio viewset
    """

    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()

    @action(detail=False, methods=["get"])
    def personal_portfolios_by_performance(self, request: Request) -> Response:
        """
        Return the matched portfolios by maximum drawdown sorted by annualized return
        Args:
            request: Request object

        Returns:
            List[PortfolioType]: List of portfolios
        """
        user = request.user
        if username := request.query_params.get("username"):
            user = User.objects.get(username=username)
        age = request.query_params.get("age")
        personal_max_drawdown = get_personal_max_drawdown(user, age)
        portfolios = (
            Portfolio.objects.filter(
                backtest_data__max_drawdown__gte=personal_max_drawdown,
                backtest_data__start_date__lte=date(
                    date.today().year - 15, date.today().month, date.today().day
                ),
            )
            .order_by("-backtest_data__cagr")
            .select_related()[:10]
        )
        portfolios = self.get_serializer(portfolios, many=True).data
        return Response(
            {"personal_max_drawdown": personal_max_drawdown, "portfolios": portfolios}
        )
