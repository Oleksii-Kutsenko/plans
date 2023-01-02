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


class BaseCountryRatingComponent(models.Model):
    """
    Base Index Data model
    """

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="%(class)s"
    )
    value = models.FloatField()
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
        return f"{self.country} {self.value} {self.year}"

    @classmethod
    def get_latest_available_data_year(cls) -> int:
        """
        Returns the latest available year for rating component data
        Returns:
            int: latest available year for rating component data
        """
        return cls.objects.latest("year").year


class CountryEconomicFreedomIndex(BaseCountryRatingComponent):
    """
    Country Economic Freedom Index model
    """


class CountryPayingTaxesIndex(BaseCountryRatingComponent):
    """
    Country Paying Taxes Index model
    """


class CountrySuicideRate(BaseCountryRatingComponent):
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

    @staticmethod
    def get_latest_available_data_year() -> int:
        """
        Returns latest available data year
        Returns:
            int: year
        """
        return ReserveCurrency.objects.latest("year").year


class CountryGDP(BaseCountryRatingComponent):
    """
    Country GDP
    """


class CountryGlobalFinancialCenterIndex(BaseCountryRatingComponent):
    """
    Country Global Financial Center Index
    """


class CountryExportsValue(BaseCountryRatingComponent):
    """
    Country Exports value in millions of USD
    """


class CountryTotalTradeValue(BaseCountryRatingComponent):
    """
    Country Imports value in millions of USD
    """


class CountryMilitaryStrength(BaseCountryRatingComponent):
    """
    Country Military Strength
    """


class CountryNatureIndex(BaseCountryRatingComponent):
    """
    Country Nature Index
    """


class CountryPisaScore(BaseCountryRatingComponent):
    """
    Country Pisa Score
    """


class CountryPassportIndex(BaseCountryRatingComponent):
    """
    Country Passport Index
    """
