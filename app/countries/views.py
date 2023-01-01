from typing import Any

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from countries.country_rating_calculator import CountryRatingCalculator
from countries.models import (
    Country,
)
from countries.serializers import CountrySerializer


class CountryViewSet(viewsets.ModelViewSet):
    """
    List of countries with their average economic freedom and paying taxes normalized index scores.
    """

    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        country_rating_calculator = CountryRatingCalculator()
        return Response(country_rating_calculator.dataframe.to_dict("records"))
