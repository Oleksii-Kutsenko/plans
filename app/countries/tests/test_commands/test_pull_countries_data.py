from typing import Dict, Any

import pandas as pd
from django.core.management import call_command
from django.test import TestCase

from countries.management.commands.pull_countries_data import Command
from countries.models import CountryEconomicFreedomIndex


class PullCountriesDataTestCase(TestCase):
    """
    TestCases for pull_countries_data command
    """

    def test_pull_countries_data(self) -> None:
        """
        Test that pull_countries_data command creates CountryEconomicFreedomIndex objects
        Returns:
            None
        """
        dataframe = pd.read_excel(Command.OLD_ECONOMIC_FREEDOM_INDEX_DATA)

        args = ["--dump-data"]
        opts: Dict[str, Any] = {}
        call_command("pull_countries_data", *args, **opts)

        self.assertEqual(CountryEconomicFreedomIndex.objects.count(), len(dataframe))
        dumped_dataframe = pd.read_excel(Command.OLD_ECONOMIC_FREEDOM_INDEX_DATA)

        assert dumped_dataframe.equals(dataframe)
