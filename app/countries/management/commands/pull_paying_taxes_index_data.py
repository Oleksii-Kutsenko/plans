from pathlib import Path
from typing import Any

import pandas as pd
import pycountry
from django.core.management.base import BaseCommand

from countries.models import CountryPayingTaxesIndex, Country

COUNTRIES_MAPPING = {
    "Korea, Rep.": "Korea, Republic of",
    "Bahamas, The": "Bahamas",
    "Liechtenstein*": "Liechtenstein",
    "St. Lucia": "Saint Lucia",
    "Yemen, Rep.": "Yemen",
    "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    "Micronesia, Fed. Sts.": "Micronesia, Federated States of",
    "St. Kitts and Nevis": "Saint Kitts and Nevis",
    "Iran, Islamic Rep.": "Iran, Islamic Republic of",
    "Egypt, Arab Rep.": "Egypt",
    "Lao PDR": "Lao People's Democratic Republic",
    "Gambia, The": "Gambia",
    "Congo, Dem. Rep.": "Congo, The Democratic Republic of the",
    "Congo, Rep.": "Republic of the Congo",
    "Venezuela, RB": "Venezuela, Bolivarian Republic of",
    "Niger": "Republic of the Niger",
}


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
        for _, row in taxes_dataframe.iterrows():
            # skip headers
            if row["Unnamed: 0"] == "Region" or row["Unnamed: 0"] == "Location":
                continue

            # check problematic countries
            country_name = row["Location"]
            if row["Location"] in COUNTRIES_MAPPING:
                country_name = COUNTRIES_MAPPING[row["Location"]]

            if country_name == "Kosovo":
                # Skip unrecognized territory
                continue

            country_paying_taxes_index_objects = []
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

            CountryPayingTaxesIndex.objects.bulk_create(
                country_paying_taxes_index_objects
            )
