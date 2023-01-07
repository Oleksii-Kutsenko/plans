import pandas as pd
from django.core.management import call_command
from django.db.models import Sum
from django.test import TestCase

from countries.management.commands.pull_suicide_rates_data import Command
from countries.models import CountrySuicideRate


class PullSuicideRatesDataCommandTestCases(TestCase):
    """
    Tests cases for the pull_suicide_rates_data command
    """

    def test_pull_suicide_rates_data_command(self) -> None:
        """
        Tests that pull_suicide_rates_data command parses all available data
        Returns:
            None
        """
        suicide_dataframe = pd.read_csv(Command.SUICIDE_RATES_DATA_PATH, skiprows=1)
        value_column_name = suicide_dataframe.columns[-1]
        suicide_rate_dataframe = pd.DataFrame(suicide_dataframe[value_column_name].str.split(" ").tolist())
        suicide_rate_dataframe[0] = suicide_rate_dataframe[0].astype(float
                                                                     )
        suicide_rates_total = suicide_rate_dataframe[0].sum()
        suicide_rates_count = len(suicide_rate_dataframe)

        call_command("pull_suicide_rates_data")

        self.assertAlmostEqual(
            CountrySuicideRate.objects.aggregate(Sum("value")).get("value__sum"),
            suicide_rates_total,
            places=2,
        )
        self.assertEqual(CountrySuicideRate.objects.count(), suicide_rates_count)
