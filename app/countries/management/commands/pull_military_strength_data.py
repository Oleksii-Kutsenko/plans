from typing import Any

import pycountry
import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand

from countries.management.commands.counties_mapping import (
    MappingSolver,
    territories_regions_unrecognized_countries,
)
from countries.models import Country, CountryMilitaryStrength


class Command(BaseCommand):
    """
    Command that fetches countries Military Strength data from HTML page
    """

    help = "Pulls Global Firepower Military Strength Data"
    MILITARY_STRENGTH_DATA_PATH = (
        "https://www.globalfirepower.com/countries-listing.php"
    )

    def handle(self, *args: Any, **options: Any) -> None:
        response = requests.get(self.MILITARY_STRENGTH_DATA_PATH, timeout=5)
        beautiful_soup = BeautifulSoup(response.text, "html.parser")
        if title := beautiful_soup.find("title"):
            year = int(title.text.split(" ")[0])
        else:
            raise ValueError("Could not find title in response")

        raw_military_strength_data = self.get_raw_military_strength_data(beautiful_soup, year)

        CountryMilitaryStrength.objects.filter(year=year).delete()
        self.create_countries_military_strength_objects(raw_military_strength_data)

    @staticmethod
    def get_raw_military_strength_data(
        beautiful_soup: BeautifulSoup, year: int
    ) -> list[tuple[str, int, float]]:
        """
        Parses HTML page and returns raw military strength data
        Args:
            year: Index year
            beautiful_soup: BeautifulSoup object

        Returns:
            list[tuple[str, int, float]]: list of tuples with country name, military strength rank
             and military strength score
        """
        military_strength_raw_data = []
        raw_data_rows = beautiful_soup.select(".picTrans.recordsetContainer.boxShadow")
        for raw_data_row in raw_data_rows:
            if raw_country_name_tag := raw_data_row.select_one(
                ".textWhite.textLarge.textShadow"
            ):
                raw_country_name = raw_country_name_tag.text.strip()
            else:
                raise ValueError("Could not find country name in country row")
            if raw_country_name in territories_regions_unrecognized_countries:
                continue
            country_name = MappingSolver.get_country_name(raw_country_name)
            country = pycountry.countries.search_fuzzy(country_name)[0]

            if raw_military_strength_tag := raw_data_row.select_one(".textLarge.textLtGray"):
                military_strength = float(
                    raw_military_strength_tag.text.strip().split(":")[1].strip()
                )
            else:
                raise ValueError("Could not find military strength in country row")
            military_strength_raw_data.append(
                (country.alpha_3, year, military_strength)
            )
        return military_strength_raw_data

    @staticmethod
    def create_countries_military_strength_objects(
        military_strength_raw_data: list[tuple[str, int, float]]
    ) -> None:
        """
        Creates CountryMilitaryStrength objects
        Args:
            military_strength_raw_data: List of tuples with country alpha_3, year and military
             strength

        Returns:
            None
        """
        country_codes = dict(Country.objects.values_list("iso_code", "id"))
        country_military_strength_objects = []
        for country_iso_code, year, military_strength in military_strength_raw_data:
            country_military_strength_objects.append(
                CountryMilitaryStrength(
                    country_id=country_codes[country_iso_code],
                    value=military_strength,
                    year=year,
                )
            )
        CountryMilitaryStrength.objects.bulk_create(country_military_strength_objects)
