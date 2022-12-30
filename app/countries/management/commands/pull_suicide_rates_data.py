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

    SUICIDE_RATES_DATA_YEAR = 2019
    SUICIDE_RATES_DATA_PATH = Path(
        "countries/management/commands/data/suicide_rates.xlsx"
    )
    help = "Populate suicide rates from Excel file"

    def handle(self, *args: Any, **options: Any) -> None:
        suicide_dataframe = pd.read_excel(self.SUICIDE_RATES_DATA_PATH, header=None)

        CountrySuicideRate.objects.all().delete()
        country_suicide_rate_objects = []

        for _, row in suicide_dataframe.iterrows():
            country_name = MappingSolver.get_country_name(row[0])

            try:
                search_results = pycountry.countries.search_fuzzy(country_name)
                country = Country.objects.get(
                    iso_code=search_results[0].alpha_3, name=search_results[0].name
                )

                country_suicide_rate_objects.append(
                    CountrySuicideRate(
                        country_id=country.id,
                        value=row[1],
                        year=self.SUICIDE_RATES_DATA_YEAR,
                    )
                )
            except LookupError as error:
                print(f"Country {row[0]} not found. Reason: {error}")

        CountrySuicideRate.objects.bulk_create(country_suicide_rate_objects)
