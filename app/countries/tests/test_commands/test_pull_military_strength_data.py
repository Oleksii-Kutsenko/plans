import random
from datetime import date

from django.test import TestCase

from countries.management.commands.pull_military_strength_data import Command
from countries.models import CountryMilitaryStrength, Country


class PullMilitaryStrengthDataCommandTestCases(TestCase):
    """
    Tests for the pull_military_strength_data command
    """

    def test_create_countries_military_strength_objects(self):
        countries_iso_codes = list(Country.objects.values_list("iso_code", flat=True))
        expected_countries_iso_codes = list(random.sample(countries_iso_codes, 10))
        year = date.today().year
        expected_value = 0.10
        test_military_strength_raw_data = [
            (country_iso_code, year, expected_value)
            for country_iso_code in expected_countries_iso_codes
        ]

        Command.create_countries_military_strength_objects(
            test_military_strength_raw_data
        )

        for country_military_strength in CountryMilitaryStrength.objects.all():
            self.assertIn(
                country_military_strength.country.iso_code, expected_countries_iso_codes
            )
            self.assertEqual(country_military_strength.value, expected_value)
            self.assertEqual(country_military_strength.year, year)
