import pandas as pd
from django.core.management import call_command
from django.test import TestCase

from countries.management.commands.counties_mapping import (
    territories_regions_unrecognized_countries,
)
from countries.management.commands.pull_passport_index_data import Command
from countries.models import CountryPassportIndex


class PullPassportIndexDataTestCases(TestCase):
    """
    Tests for the pull_passport_index_data command
    """

    def test_pull_passport_index_data_command(self) -> None:
        """
        Test that the command pulls data from the passport index Excel file and saves it to the database
        Returns:
            None
        """
        passport_index_dataframe = pd.read_excel(
            Command.PASSPORT_INDEX_DATA_PATH, header=None, names=["country", "score"]
        )
        passport_index_dataframe["country"] = passport_index_dataframe[
            "country"
        ].str.strip()
        passport_index_dataframe.query(
            "country not in @territories_regions_unrecognized_countries", inplace=True
        )
        expected_passport_index_objects_number = len(passport_index_dataframe)

        call_command("pull_passport_index_data")

        self.assertEqual(
            expected_passport_index_objects_number, CountryPassportIndex.objects.count()
        )
