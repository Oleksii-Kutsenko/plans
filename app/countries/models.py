"""
Countries models
"""
import pycountry
from django.db import models

country_iso_codes = [
    (country.alpha_3, country.alpha_3) for country in pycountry.countries
]
known_reserve_currencies = [
    ("USD", "USD"),
    ("EUR", "EUR"),
    ("CNY", "CNY"),
    ("JPY", "JPY"),
    ("GBP", "GBP"),
    ("AUD", "AUD"),
    ("CAD", "CAD"),
    ("CHF", "CHF"),
]


class Country(models.Model):
    """
    Country model
    """

    name = models.CharField(max_length=255)
    iso_code = models.CharField(max_length=4, unique=True, choices=country_iso_codes)

    def __str__(self) -> str:
        return f"{self.name}"


class BaseIndexData(models.Model):
    """
    Base Index Data model
    """

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="%(class)s"
    )
    score = models.FloatField()
    year = models.IntegerField()

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["country", "year"],
                name="%(app_label)s_%(class)s_unique_country_year",
            )
        ]

    def __str__(self) -> str:
        return f"{self.country} {self.score} {self.year}"


class CountryEconomicFreedomIndex(BaseIndexData):
    """
    Country Economic Freedom Index model
    """


class CountryPayingTaxesIndex(BaseIndexData):
    """
    Country Paying Taxes Index model
    """


class CountrySuicideRate(BaseIndexData):
    """
    Country Suicide Rate model
    """


class ReserveCurrency(models.Model):
    """
    Model for storing data about known reserve currencies
    """

    symbol = models.CharField(
        max_length=3, choices=known_reserve_currencies, unique=True
    )
    percentage_in_world_reserves = models.FloatField()
    year = models.IntegerField()

    def __str__(self) -> str:
        return str(self.symbol)


class CountryReserveCurrency(models.Model):
    """
    Represents which reserve currency which country uses
    """

    country = models.OneToOneField(
        Country, on_delete=models.PROTECT, related_name="reserve_currency"
    )
    reserve_currency = models.ForeignKey(ReserveCurrency, on_delete=models.PROTECT)
