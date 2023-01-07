from pathlib import Path
from typing import Any

import pandas as pd
import pycountry
from django.core.management import BaseCommand

from countries.management.commands.counties_mapping import MappingSolver
from countries.models import CountrySuicideRate, Country


class Command(BaseCommand):
    """
    Command that fetches countries suicide rates from Excel file
    """

    SUICIDE_RATES_DATA_PATH = Path(
        "countries/management/commands/data/suicide_rates.csv"
    )
    help = "Populate suicide rates from Excel file"

    def handle(self, *args: Any, **options: Any) -> None:
        suicide_dataframe = pd.read_csv(self.SUICIDE_RATES_DATA_PATH, skiprows=1)
        if isinstance(suicide_dataframe.columns[-1], str):
            suicide_rates_data_year = int(suicide_dataframe.columns[-1])
        else:
            raise Exception("Cannot determine dataset year")

        country_suicide_rate_objects = []
        countries_codes = dict(Country.objects.values_list("iso_code", "id"))
        for row in suicide_dataframe.itertuples(index=False):
            country_name = MappingSolver.get_country_name(row[0])

            search_result = pycountry.countries.search_fuzzy(country_name)[0]
            country_id = countries_codes[search_result.alpha_3]

            suicide_rate = row[2].split(" ")[0]
            country_suicide_rate_objects.append(
                CountrySuicideRate(
                    country_id=country_id,
                    value=suicide_rate,
                    year=suicide_rates_data_year,
                )
            )

        CountrySuicideRate.objects.filter(year=suicide_rates_data_year).delete()
        CountrySuicideRate.objects.bulk_create(country_suicide_rate_objects)
