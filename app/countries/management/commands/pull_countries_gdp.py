from datetime import date
from pathlib import Path

import pandas as pd
import pycountry
from django.core.management import BaseCommand

from countries.management.commands.counties_mapping import (
    ProblematicCountriesSolver,
    territories_regions_unrecognized_countries,
)
from countries.models import Country, CountryGDP


class Command(BaseCommand):
    """
    Pull countries GDP data
    """

    GDP_DATA_PATH = Path("countries/management/commands/data/gdp.xls")
    COUNTRY_NAMES_COLUMN = "GDP, current prices (Billions of U.S. dollars)"

    def handle(self, *args, **options) -> None:
        """
        Pull countries GDP data
        Args:
            *args: arguments
            **options: options
        Returns:
            None
        """
        gdp_dataframe = pd.read_excel(self.GDP_DATA_PATH)

        current_year = date.today().year

        gdp_dataframe = gdp_dataframe[[self.COUNTRY_NAMES_COLUMN, current_year]]
        gdp_dataframe.dropna(inplace=True)

        CountryGDP.objects.all().delete()
        for _, row in gdp_dataframe.iterrows():
            raw_country_name = row[self.COUNTRY_NAMES_COLUMN].strip()
            if (
                pd.isna(row[current_year])
                or row[current_year] == "no data"
            ):
                continue

            if raw_country_name in territories_regions_unrecognized_countries:
                # skip territories and regions
                continue

            raw_country_name = ProblematicCountriesSolver.get_country_name(
                raw_country_name
            )
            search_results = pycountry.countries.search_fuzzy(raw_country_name)

            country_name = search_results[0].name
            country_iso_code = search_results[0].alpha_3

            country, _ = Country.objects.get_or_create(
                name=country_name, iso_code=country_iso_code
            )
            CountryGDP.objects.create(
                country=country,
                value=row[current_year],
                year=current_year,
            )
