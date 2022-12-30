from unittest import TestCase

import pandas as pd
from django.core.management import call_command

from countries.management.commands.pull_export_data import Command
from countries.models import CountryExportsValue, Country


class PullExportDataTestCases(TestCase):
    def test_pull_export_data(self):
        country_codes = Country.objects.values_list("iso_code", flat=True)
        dataframe = pd.read_csv(Command.EXPORT_DATA_PATH)
        expected_export_data_number = len(
            dataframe.query("`Reporting Economy ISO3A Code` in @country_codes")
        )

        call_command("pull_export_data")

        self.assertEqual(
            CountryExportsValue.objects.count(), expected_export_data_number
        )
