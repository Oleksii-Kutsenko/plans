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

        max_economic_freedom_value = countries_dataframe["economic_freedom"].max()
        min_economic_freedom_value = countries_dataframe["economic_freedom"].min()
        countries_dataframe["economic_freedom_score"] = (
            countries_dataframe["economic_freedom"] - min_economic_freedom_value
        ) / (max_economic_freedom_value - min_economic_freedom_value)

        max_paying_taxes_value = countries_dataframe["paying_taxes"].max()
        min_paying_taxes_value = countries_dataframe["paying_taxes"].min()
        countries_dataframe["paying_taxes_score"] = (
            countries_dataframe["paying_taxes"] - min_paying_taxes_value
        ) / (max_paying_taxes_value - min_paying_taxes_value)

        max_suicide_rate_value = countries_dataframe["suicide_rate"].max()
        min_suicide_rate_value = countries_dataframe["suicide_rate"].min()
        countries_dataframe["suicide_rate_score"] = (
            countries_dataframe["suicide_rate"] - min_suicide_rate_value
        ) / (max_suicide_rate_value - min_suicide_rate_value)
        countries_dataframe = countries_dataframe.fillna(0)
        countries_dataframe["suicide_rate_score"] = (
            1 - countries_dataframe["suicide_rate_score"]
        )

        countries_dataframe["total_score"] = countries_dataframe[
            ["economic_freedom_score", "paying_taxes_score", "suicide_rate_score"]
        ].mean(axis=1)
        countries_dataframe = countries_dataframe.sort_values(
            by="total_score", ascending=False
        )

        print(countries_dataframe)

        return Response(countries_dataframe.to_dict("records"))
