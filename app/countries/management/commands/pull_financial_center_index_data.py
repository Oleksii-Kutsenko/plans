import re
from pathlib import Path
from typing import Any

import geonamescache
import pycountry
from django.core.management.base import BaseCommand
from pypdf import PdfReader, PageObject

from countries.management.commands.counties_mapping import (
    MappingSolver,
    territories_regions_unrecognized_countries,
)
from countries.models import CountryGlobalFinancialCenterIndex, Country


class Command(BaseCommand):
    """
    Command that fetches countries Global Financial Center Index data
    """

    GFCI_DATA_PATH = Path(
        "countries/management/commands/data/GFCI_32_Report_2022.09.22_v1.0_.pdf"
    )
    GFCI_DATA_YEAR = 2022
    RATING_EXTRACTION_REGEX = r"^[a-zA-Z-' ]* {current_index} \d\d\d"

    def handle(self, *args: tuple[Any], **options: dict[str, Any]) -> None:
        pages = self.get_pages()
        matches = self.extract_matches(pages)
        countries_rating = self.replace_cities_with_countries(matches)

        countries_rating_total = {}
        for country_name, country_iso_code, rating in countries_rating:
            country_identifier = f"{country_name}/{country_iso_code}"
            if country_identifier not in countries_rating_total:
                countries_rating_total[country_identifier] = rating
            else:
                countries_rating_total[country_identifier] += rating

        country_gfci_objects = []
        for country_identifier, rating in countries_rating_total.items():
            country_name, country_iso_code = country_identifier.split("/")
            country_obj = Country.objects.get(
                name=country_name, iso_code=country_iso_code
            )

            country_gfci_objects.append(
                CountryGlobalFinancialCenterIndex(
                    country=country_obj, value=rating, year=self.GFCI_DATA_YEAR
                )
            )

        CountryGlobalFinancialCenterIndex.objects.all().delete()
        CountryGlobalFinancialCenterIndex.objects.bulk_create(country_gfci_objects)

    @classmethod
    def extract_matches(cls, pages: list[PageObject]) -> list[tuple[str, int]]:
        """
        Extracts city names and ratings from the pages
        Args:
            pages:

        Returns:

        """
        current_index = 1
        matches = []
        for page in pages:
            text = page.extract_text()

            for line in text.split("\n"):
                match = re.search(
                    cls.RATING_EXTRACTION_REGEX.format(current_index=current_index),
                    line,
                )

                if match:
                    matched_string = match.group()
                    city_name, raw_rating = matched_string.split(f" {current_index} ")
                    rating = int(raw_rating.strip())

                    matches.append((city_name, rating))

                    current_index += 1
        return matches

    @classmethod
    def get_pages(cls) -> list[PageObject]:
        """
        Returns proper pages from the GFCI PDf
        Returns:
            list[PageObject]: List of pages
        """
        reader = PdfReader(cls.GFCI_DATA_PATH)
        index_start_page = 5
        index_end_page = 6
        pages = reader.pages[index_start_page : index_end_page + 1]
        return pages

    @staticmethod
    def replace_cities_with_countries(
        matches: list[tuple[str, int]]
    ) -> list[tuple[str, str, int]]:
        """
        Replaces matches cities with countries names
        Args:
            matches: Matches from the PDF file

        Returns:

        """
        countries_rating = []
        geonames_cache = geonamescache.GeonamesCache()
        for city_name, rating in matches:
            city_name = MappingSolver.get_city_name(city_name.strip())

            search_results = geonames_cache.search_cities(city_name)
            if search_results:
                if len(search_results) > 1:
                    # Find the city with the highest population
                    city = sorted(
                        search_results,
                        key=lambda x: x["population"],
                        reverse=True,
                    )[0]
                else:
                    city = search_results[0]

                country = pycountry.countries.get(alpha_2=city["countrycode"])

                if country.name in territories_regions_unrecognized_countries:
                    continue

                countries_rating.append((country.name, country.alpha_3, rating))

        return countries_rating
