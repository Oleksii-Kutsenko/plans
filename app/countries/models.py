from django.db import models


class CountryEconomicFreedomIndex(models.Model):
    country_iso_code = models.CharField(max_length=4)
    country = models.CharField(max_length=100)
    score = models.FloatField()
    year = models.IntegerField()

    class Meta:
        unique_together = ("country_iso_code", "year")

    def __str__(self) -> str:
        return f"{self.country_iso_code} {self.country} {self.score} {self.year}"
