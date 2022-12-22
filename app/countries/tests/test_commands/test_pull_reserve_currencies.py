from unittest import TestCase

from django.core.management import call_command

from countries.management.commands.pull_reserve_currencies import (
    reserve_currency_countries_mapper,
)
from countries.models import ReserveCurrency, CountryReserveCurrency


class PullReserveCurrenciesTest(TestCase):
    def test_pull_reserve_currencies_command(self) -> None:
        """
        Test pull_reserve_currencies command
        Returns:
            None
        """
        expected_reserve_currencies_number = len(
            reserve_currency_countries_mapper.keys()
        )
        expected_countries_currency_objects_number = 0
        for countries in reserve_currency_countries_mapper.values():
            expected_countries_currency_objects_number += len(countries)

        call_command("pull_reserve_currencies")

        self.assertEqual(
            ReserveCurrency.objects.count(), expected_reserve_currencies_number
        )
        self.assertEqual(
            CountryReserveCurrency.objects.count(),
            expected_countries_currency_objects_number,
        )
