from datetime import date

from django.test import TestCase

from countries.management.commands.pull_military_strength_data import Command
from countries.models import CountryMilitaryStrength
from countries.tests.factories.country import CountryFactory


class PullMilitaryStrengthDataCommandTestCases(TestCase):
    def test_create_countries_military_strength_objects(self):
        year = date.today().year
        countries = CountryFactory.create_batch(3)
        expected_countries_names = [country.name for country in countries]
        expected_value = 0.10
        test_military_strength_raw_data = [
            (country.iso_code, year, expected_value) for country in countries
        ]

        Command.create_countries_military_strength_objects(
            test_military_strength_raw_data
        )

        for country_military_strength in CountryMilitaryStrength.objects.all():
            self.assertIn(
                country_military_strength.country.name, expected_countries_names
            )
            self.assertEqual(country_military_strength.value, expected_value)
            self.assertEqual(country_military_strength.year, year)
