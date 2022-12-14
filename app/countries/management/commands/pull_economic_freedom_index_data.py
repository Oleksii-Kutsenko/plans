"""
Command to pull countries data from the web page or load old data from the file
"""
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd
import pycountry
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandParser

from .counties_mapping import territories_regions_unrecognized_countries
from .html_tag_utils import HTMLTagName
from ...models import CountryEconomicFreedomIndex, Country

country_converter = {
    "Republic of Congo": "Republic of the Congo",
    "Laos": "Lao People's Democratic Republic",
    "Burma": "Republic of Myanmar",
    "Democratic Republic of Congo": "Congo, The Democratic Republic of the",
    "Niger": "Republic of the Niger",
}


class Command(BaseCommand):
    """
    Command that fetches countries Economic Freedom Index data and
    creates CountryEconomicFreedomIndex objects
    """

    ECONOMIC_FREEDOM_INDEX_DATA = Path(
        "countries/management/commands/data/economic_freedom_index.xlsx"
    )
    ECONOMIC_FREEDOM_INDEX_URL = "https://www.heritage.org/index/ranking"
    help = "Pull countries information from data sources"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--dump-data",
            action="store_true",
        )

    def handle(self, *args: tuple[Any], **options: dict[str, Any]) -> None:
        current_year = date.today().year
        self.load_economic_freedom_index_data()
        if CountryEconomicFreedomIndex.objects.filter(year=current_year).count() == 0:
            self.load_latest_economic_freedom_index_data()
        if options.get("dump_data"):
            self.dump_economic_freedom_index_data()

    def get_economic_freedom_index_data_path(self) -> Path:
        """
        Returns path to the Economic Freedom Index data file

        Returns:
            Path: Path to the Economic Freedom Index data file
        """
        return self.ECONOMIC_FREEDOM_INDEX_DATA

    def load_latest_economic_freedom_index_data(self) -> None:
        """
        Loads Economic Freedom Index ranking page and parses it

        Returns:
            None
        """
        response = requests.get(self.ECONOMIC_FREEDOM_INDEX_URL, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        try:
            data_header = soup.find_all("a", class_="brand")[0].text
            data_year = int(data_header[:4])
        except Exception as error:
            raise Exception("Unable to determinate data year") from error
        if CountryEconomicFreedomIndex.objects.filter(year=data_year).count() != 0:
            return

        country_economic_freedom_index_objects = []
        rankings_tables = soup.find_all("table", class_="rankings")
        for table in rankings_tables:
            for table_row in table.find_all([HTMLTagName.TR.value]):
                country = None
                score = None
                for table_data in table_row.find_all(
                    [HTMLTagName.TD.value, HTMLTagName.TH.value]
                ):
                    if table_data.name == HTMLTagName.TH.value:
                        # Skip header
                        break
                    if table_data["class"][0] == "country":
                        country_name = table_data.text
                        if country_name in territories_regions_unrecognized_countries:
                            # Skip unrecognized territory
                            continue
                        if country_name in country_converter:
                            country_name = country_converter.get(country_name)
                        country = pycountry.countries.search_fuzzy(country_name)[0]
                    if table_data["class"][0] == "overall":
                        try:
                            score = float(table_data.text)
                        except ValueError:
                            score = 0

                    if country and score:
                        country_obj = Country.objects.get(
                            iso_code=country.alpha_3, name=country.name
                        )
                        country_economic_freedom_index_objects.append(
                            CountryEconomicFreedomIndex(
                                country=country_obj,
                                value=score,
                                year=data_year,
                            )
                        )
                        country = None
                        score = None
        CountryEconomicFreedomIndex.objects.bulk_create(
            country_economic_freedom_index_objects
        )

    def load_economic_freedom_index_data(self) -> None:
        """
        Loads Economic Freedom Index data from the Excel file and
        creates CountryEconomicFreedomIndex objects

        Returns:
            None
        """
        eco_dataframe = pd.read_excel(self.get_economic_freedom_index_data_path())
        country_economic_freedom_index_objects = []
        for _, row in eco_dataframe.iterrows():
            if row["country__name"] in territories_regions_unrecognized_countries:
                # Skip unrecognized territory
                continue

            country = Country.objects.get(
                iso_code=row["country__iso_code"],
                name=pycountry.countries.get(alpha_3=row["country__iso_code"]).name,
            )
            country_economic_freedom_index_objects.append(
                CountryEconomicFreedomIndex(
                    country=country,
                    value=row["value"],
                    year=row["year"],
                )
            )

        CountryEconomicFreedomIndex.objects.all().delete()
        CountryEconomicFreedomIndex.objects.bulk_create(
            country_economic_freedom_index_objects
        )

    def dump_economic_freedom_index_data(self) -> None:
        """
        Dumps all available Economic Freedom Index data to the Excel file

        Returns:
            None
        """
        country_economic_freedom_index_df = pd.DataFrame(
            list(
                CountryEconomicFreedomIndex.objects.all().values(
                    "country__iso_code", "country__name", "value", "year"
                )
            )
        )
        country_economic_freedom_index_df.to_excel(
            self.get_economic_freedom_index_data_path()
        )
