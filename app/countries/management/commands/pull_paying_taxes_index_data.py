from pathlib import Path
from typing import Any

import pandas as pd
import pycountry
from django.core.management.base import BaseCommand

from countries.management.commands.counties_mapping import ProblematicCountriesSolver
from countries.models import CountryPayingTaxesIndex, Country


class Command(BaseCommand):
    """
    Command that fetches countries Paying Taxes Index data from Excel file
    """

    PAYING_TAXES_INDEX_DATA_YEAR = 2020
    PAYING_TAXES_INDEX_DATA_PATH = Path(
        "countries/management/commands/data/Paying Taxes.xlsx"
    )
    help = "Pull countries information from data sources"

    def handle(self, *args: Any, **options: Any) -> None:
        taxes_dataframe = pd.read_excel(self.PAYING_TAXES_INDEX_DATA_PATH)

        CountryPayingTaxesIndex.objects.all().delete()
        country_paying_taxes_index_objects = []
        for _, row in taxes_dataframe.iterrows():
            # skip headers
            if row["Unnamed: 0"] == "Region" or row["Unnamed: 0"] == "Location":
                continue

            country_name = ProblematicCountriesSolver.get_country_name(row["Location"])

            if country_name == "Kosovo":
                # Skip unrecognized territory
                continue

            try:
                search_results = pycountry.countries.search_fuzzy(country_name)
                country, _ = Country.objects.get_or_create(
                    iso_code=search_results[0].alpha_3, name=search_results[0].name
                )

                country_paying_taxes_index_objects.append(
                    CountryPayingTaxesIndex(
                        country_id=country.id,
                        score=row["Paying Taxes score"],
                        year=self.PAYING_TAXES_INDEX_DATA_YEAR,
                    )
                )
            except LookupError as error:
                print(f"Country {row['Location']} not found. Reason: {error}")

        CountryPayingTaxesIndex.objects.bulk_create(country_paying_taxes_index_objects)
