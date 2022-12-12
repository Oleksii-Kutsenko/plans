from django.db.models import QuerySet
from rest_framework import viewsets

from countries.models import (
    Country,
    CountryEconomicFreedomIndex,
    CountryPayingTaxesIndex,
)
from countries.serializers import CountrySerializer


class CountryViewSet(viewsets.ModelViewSet):
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
            .values(
                "name",
                "countryeconomicfreedomindex__score",
                "countryeconomicfreedomindex__year",
                "countrypayingtaxesindex__score",
                "countrypayingtaxesindex__year",
            )
        )

        return queryset
