from typing import Dict, Any
from unittest.mock import patch, MagicMock

import pandas as pd
from django.core.management import call_command
from django.test import TestCase

from countries.management.commands.pull_economic_freedom_index_data import Command
from countries.models import CountryEconomicFreedomIndex, Country


class PullCountriesDataTestCase(TestCase):
    """
    TestCases for pull_countries_data command
    """

    @patch(
        "countries.management.commands.pull_economic_freedom_index_data.Command.get_economic_freedom_index_data_path",
        return_value="/tmp/economic_freedom_index.xlsx",
    )
    def test_pull_existing_countries_data(
        self, get_economic_freedom_index_data_path_mock: MagicMock
    ) -> None:
        """
        Test that pull_countries_data command creates CountryEconomicFreedomIndex objects
        Returns:
            None
        """
        dataframe = pd.read_excel(Command.ECONOMIC_FREEDOM_INDEX_DATA)
        dataframe.to_excel(get_economic_freedom_index_data_path_mock())

        args = ["--dump-data"]
        opts: Dict[str, Any] = {}
        call_command("pull_economic_freedom_index_data", *args, **opts)

        self.assertEqual(CountryEconomicFreedomIndex.objects.count(), len(dataframe))
        dumped_dataframe = pd.read_excel(Command.ECONOMIC_FREEDOM_INDEX_DATA)

        assert dumped_dataframe.equals(dataframe)

    @patch(
        "countries.management.commands.pull_economic_freedom_index_data.Command.load_economic_freedom_index_data",
        return_value=None,
    )
    def test_pull_new_countries_data(self, _: MagicMock) -> None:
        """
        Test that pull_countries_data command parses Economic Freedom Index web page correctly
        Returns:
            None
        """
        expected_countries_number = 176
        expected_index_data_number = 176
        call_command("pull_economic_freedom_index_data")

        self.assertEqual(Country.objects.count(), expected_countries_number)
        self.assertEqual(
            CountryEconomicFreedomIndex.objects.count(), expected_index_data_number
        )
