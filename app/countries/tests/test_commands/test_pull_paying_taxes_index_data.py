from unittest import TestCase

import pandas as pd
import pycountry
from django.core.management import call_command

from countries.management.commands.counties_mapping import ProblematicCountriesSolver
from countries.management.commands.pull_paying_taxes_index_data import Command
from countries.models import CountryPayingTaxesIndex


class PullPayingTaxesIndexDataTest(TestCase):
    def test_command_output(self):
        taxes_dataframe = pd.read_excel(Command.PAYING_TAXES_INDEX_DATA_PATH)
        expected_index_data_number = 0
        for _, row in taxes_dataframe.iterrows():
            try:
                if row["Unnamed: 0"] == "Region" or row["Unnamed: 0"] == "Location":
                    continue
                country_name = ProblematicCountriesSolver.get_country_name(
                    row["Location"]
                )
                if country_name == "Kosovo":
                    # Skip unrecognized territory
                    continue
                search_results = pycountry.countries.search_fuzzy(country_name)
                expected_index_data_number += 1
            except LookupError:
                continue

        call_command("pull_paying_taxes_index_data")

        self.assertEqual(
            expected_index_data_number, CountryPayingTaxesIndex.objects.count()
        )
