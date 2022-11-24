from unittest import TestCase

import pandas as pd
from django.core.management import call_command

from countries.management.commands.pull_countries_data import Command
from countries.models import CountryEconomicFreedomIndex


class PullCountriesDataTestCase(TestCase):
    def test_pull_countries_data(self) -> None:
        """
        Test that pull_countries_data command creates CountryEconomicFreedomIndex objects
        Returns:
            None
        """
        dataframe = pd.read_excel(Command.OLD_ECONOMIC_FREEDOM_INDEX_DATA)
        call_command("pull_countries_data")
        self.assertEqual(CountryEconomicFreedomIndex.objects.count(), len(dataframe))
