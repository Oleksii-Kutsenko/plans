from typing import Any

import pandas as pd
from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from countries.models import (
    Country,
    CountryEconomicFreedomIndex,
    CountryPayingTaxesIndex,
)
from countries.serializers import CountrySerializer


class CountryViewSet(viewsets.ModelViewSet):
    """
    List of countries with their average economic freedom and paying taxes normalized index scores.
    """
    serializer_class = CountrySerializer

    def get_queryset(self) -> QuerySet:
        latest_economic_freedom_index_year = CountryEconomicFreedomIndex.objects.latest(
            "year"
        ).year
        latest_paying_taxes_index_year = CountryPayingTaxesIndex.objects.latest(
            "year"
        ).year

        queryset = (
            Country.objects.prefetch_related(
                "countryeconomicfreedomindex", "countrypayingtaxesindex"
            )
            .filter(
                countryeconomicfreedomindex__year=latest_economic_freedom_index_year,
                countrypayingtaxesindex__year=latest_paying_taxes_index_year,
            )
            .values_list(
                "name",
                "countryeconomicfreedomindex__score",
                "countryeconomicfreedomindex__year",
                "countrypayingtaxesindex__score",
                "countrypayingtaxesindex__year",
            )
        )

        return queryset

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = list(self.get_queryset())
        countries_dataframe = pd.DataFrame(
            data,
            columns=[
                "name",
                "economic_freedom",
                "economic_freedom_year",
                "paying_taxes",
                "paying_taxes_year",
            ],
        )
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

        countries_dataframe["total_score"] = countries_dataframe[
            ["economic_freedom_score", "paying_taxes_score"]
        ].mean(axis=1)
        countries_dataframe = countries_dataframe.sort_values(
            by="total_score", ascending=False
        )

        return Response(countries_dataframe.to_dict("records"))
