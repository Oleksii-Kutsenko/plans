from pathlib import Path
from typing import Any

import pandas as pd
import pycountry
from django.core.management.base import BaseCommand

from countries.management.commands.counties_mapping import (
    territories_regions_unrecognized_countries,
    MappingSolver,
)
from countries.models import Country, CountryPassportIndex


class Command(BaseCommand):
    """
    Pull data from the passport index Excel file and save it to the database
    """

    PASSPORT_INDEX_DATA_PATH = Path(
        "countries/management/commands/data/passport_index_data.xlsx"
    )
    PASSPORT_INDEX_DATA_YEAR = 2022

    def handle(self, *args: Any, **options: Any) -> None:
        passport_index_dataframe = pd.read_excel(
            self.PASSPORT_INDEX_DATA_PATH, header=None, names=["country", "score"]
        )

        countries_codes = dict(Country.objects.values_list("iso_code", "id"))
        country_passport_index_objects = []
        for row in passport_index_dataframe.itertuples():
            raw_country_name = row.country.strip()
            if raw_country_name in territories_regions_unrecognized_countries:
                continue
            raw_country_name = MappingSolver.get_country_name(raw_country_name)
            country = pycountry.countries.search_fuzzy(raw_country_name)[0]

            score = int(row.score)

            country_passport_index_objects.append(
                CountryPassportIndex(
                    country_id=countries_codes[country.alpha_3],
                    value=score,
                    year=self.PASSPORT_INDEX_DATA_YEAR,
                )
            )

        CountryPassportIndex.objects.all().delete()
        CountryPassportIndex.objects.bulk_create(country_passport_index_objects)
