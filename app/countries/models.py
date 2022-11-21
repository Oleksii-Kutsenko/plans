import pycountry
from django.db import models

country_iso_codes = [(country.alpha_3, country.alpha_3) for country in pycountry.countries]


class Country(models.Model):
    """
    Country model
    """
    name = models.CharField(max_length=255)
    iso_code = models.CharField(max_length=4, unique=True, choices=country_iso_codes)

    def __str__(self):
        return self.name


class CountryEconomicFreedomIndex(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    score = models.FloatField()
    year = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.country} {self.score} {self.year}"
