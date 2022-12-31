from typing import Any

import bs4
import pycountry
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from countries.management.commands.counties_mapping import (
    territories_regions_unrecognized_countries,
    MappingSolver,
)
from countries.management.commands.html_tag_utils import HTMLTagName
from countries.models import Country, CountryNatureIndex


class Command(BaseCommand):
    """
    Command that fetches countries Nature Index data from HTML page
    """

    help = "Pulls data from Nature Index HTML page"
    NATURE_INDEX_DATA_PATH = (
        "https://www.nature.com/nature-index/country-outputs/generate/all/global"
    )

    def handle(self, *args: Any, **options: Any) -> None:
        response = requests.get(self.NATURE_INDEX_DATA_PATH, timeout=5)
        beautiful_soup = BeautifulSoup(response.text, "html.parser")

        raw_nature_index_data = self.get_raw_nature_index_data(beautiful_soup)

        country_codes = dict(Country.objects.values_list("iso_code", "id"))
        country_nature_index_data = []
        for code, year, share in raw_nature_index_data:
            country_nature_index_data.append(
                CountryNatureIndex(
                    country_id=country_codes[code], year=year, value=share
                )
            )

        CountryNatureIndex.objects.all().delete()
        CountryNatureIndex.objects.bulk_create(country_nature_index_data)

    @staticmethod
    def get_raw_nature_index_data(
        beautiful_soup: bs4.BeautifulSoup,
    ) -> list[tuple[str, int, float]]:
        """
        Extracts raw data from HTML page
        Args:
            beautiful_soup: BeautifulSoup object with Nature Index HTML page

        Returns:
            List of tuples with country code, year and share (value)
        """
        if date_range_tage := beautiful_soup.select_one(".font-weight-light"):
            date_range = date_range_tage.text
            year = int(date_range.split(" ")[-1])
        else:
            raise ValueError("Date range tag not found")
        if table_tag := beautiful_soup.select_one("#simpleTable"):
            table_body = table_tag.find(HTMLTagName.TBODY.value)
            if not isinstance(table_body, bs4.Tag):
                raise ValueError("Table body not found")
        else:
            raise ValueError("Table tag not found")
        raw_nature_index_data = []
        for tr_tag in table_body.find_all(HTMLTagName.TR.value):
            _, raw_country_name, _, share = [
                td.text for td in tr_tag.find_all(HTMLTagName.TD.value)
            ]
            if raw_country_name == "United States":
                # Index error
                continue
            if raw_country_name in territories_regions_unrecognized_countries:
                continue
            country_name = MappingSolver.get_country_name(raw_country_name)
            country = pycountry.countries.search_fuzzy(country_name)[0]

            raw_nature_index_data.append((str(country.alpha_3), year, float(share)))
        return raw_nature_index_data
