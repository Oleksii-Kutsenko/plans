from unittest import TestCase

import pycountry
from django.core.management import call_command

from countries.management.commands.counties_mapping import (
    ProblematicCountriesSolver,
)
from countries.management.commands.pull_paying_taxes_index_data import Command
from countries.models import CountryPayingTaxesIndex


class PullPayingTaxesIndexDataTest(TestCase):
    def test_pull_paying_taxes_index_data_command(self) -> None:
        """
        Test pull_paying_taxes_index_data command
        Returns:
            None
        """
        taxes_dataframe = Command.process_taxes_dataframe(
            Command.PAYING_TAXES_INDEX_DATA_PATH
        )

        expected_index_data_number = 0
        for _, row in taxes_dataframe.iterrows():
            country_name = ProblematicCountriesSolver.get_country_name(row["Location"])
            pycountry.countries.search_fuzzy(country_name)
            expected_index_data_number += 1

        call_command("pull_paying_taxes_index_data")

        self.assertEqual(
            expected_index_data_number, CountryPayingTaxesIndex.objects.count()
        )
