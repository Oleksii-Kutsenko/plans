from pathlib import Path
from typing import Any

import pandas as pd
import pycountry
from django.core.management.base import BaseCommand

from countries.management.commands.counties_mapping import (
    MappingSolver,
    territories_regions_unrecognized_countries,
)
from countries.models import CountryPisaScore, Country


class Command(BaseCommand):
    """
    Pulls PISA scores from Excel file and saves them to database
    """

    PISA_DATA_PATH = Path("countries/management/commands/data/pisa.xlsx")
    PISA_DATA_YEAR = 2018

    def handle(self, *args: Any, **options: Any) -> None:
        pisa_dataframe = pd.read_excel(
            self.PISA_DATA_PATH, header=None, names=["country", "score"]
        )

        countries_codes = dict(Country.objects.values_list("iso_code", "id"))
        country_pisa_score_objects = []
        for row in pisa_dataframe.itertuples():
            raw_country_name = row.country
            if raw_country_name in territories_regions_unrecognized_countries:
                continue
            raw_country_name = MappingSolver.get_country_name(raw_country_name)
            country = pycountry.countries.search_fuzzy(raw_country_name)[0]

            score = float(row.score)

            country_pisa_score_objects.append(
                CountryPisaScore(
                    country_id=countries_codes[country.alpha_3],
                    value=score,
                    year=self.PISA_DATA_YEAR,
                )
            )

        CountryPisaScore.objects.all().delete()
        CountryPisaScore.objects.bulk_create(country_pisa_score_objects)
