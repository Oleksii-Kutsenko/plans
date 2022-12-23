from datetime import date
from unittest import TestCase

import pandas as pd
from django.core.management import call_command

from countries.management.commands.counties_mapping import (
    territories_regions_unrecognized_countries,
)
from countries.management.commands.pull_countries_gdp import Command
from countries.models import CountryGDP


class PullCountriesGDPTestCase(TestCase):
    """
    Test pull_countries_gdp command
    Returns:
        None
    """

    def test_command_output(self) -> None:
        expected_country_gdp_objects_number = 0
        gdp_dataframe = pd.read_excel(Command.GDP_DATA_PATH)

        current_year = date.today().year

        gdp_dataframe = gdp_dataframe[[Command.COUNTRY_NAMES_COLUMN, current_year]]
        gdp_dataframe.dropna(inplace=True)
        for _, row in gdp_dataframe.iterrows():
            raw_country_name = row[Command.COUNTRY_NAMES_COLUMN].strip()
            if (
                pd.isna(row[current_year])
                or row[current_year] == "no data"
            ):
                continue

            if raw_country_name in territories_regions_unrecognized_countries:
                # skip territories and regions
                continue

            expected_country_gdp_objects_number += 1

        call_command("pull_countries_gdp")

        self.assertEqual(
            CountryGDP.objects.count(), expected_country_gdp_objects_number
        )
