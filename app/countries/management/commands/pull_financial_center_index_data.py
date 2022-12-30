import re
from pathlib import Path
from typing import Any

import geonamescache
import pycountry
from django.core.management.base import BaseCommand
from pypdf import PdfReader, PageObject

from countries.management.commands.counties_mapping import MappingSolver
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
        geonames_cache = geonamescache.GeonamesCache()

        pages = self.get_pages()
        matches = self.extract_matches(pages)

        country_rating = {}
        for city_name, rating in matches:
            city_name = MappingSolver.get_city_name(city_name.strip())

            search_results = geonames_cache.search_cities(city_name)
            if search_results:
                if len(search_results) > 1:
                    # Find the city with the highest population
                    country = sorted(
                        search_results,
                        key=lambda x: x["population"],
                        reverse=True,
                    )[0]
                else:
                    country = search_results[0]

                country_name = pycountry.countries.get(
                    alpha_2=country["countrycode"]
                ).name

                if country_name == "Hong Kong":
                    country_name = "China"
                elif country_name == "Guernsey":
                    country_name = "United Kingdom"
                elif country_name == "Gibraltar":
                    country_name = "United Kingdom"
                elif country_name == "Virgin Islands, British":
                    country_name = "United Kingdom"

                if country_name not in country_rating:
                    country_rating[country_name] = rating
                else:
                    country_rating[country_name] += rating

        CountryGlobalFinancialCenterIndex.objects.all().delete()

        country_gfci_objects = []
        for country_name, rating in country_rating.items():
            country = pycountry.countries.get(name=country_name)
            country_obj, _ = Country.objects.get_or_create(
                name=country.name, iso_code=country.alpha_3
            )
            country_gfci_objects.append(
                CountryGlobalFinancialCenterIndex(
                    country=country_obj, value=rating, year=self.GFCI_DATA_YEAR
                )
            )
        CountryGlobalFinancialCenterIndex.objects.bulk_create(country_gfci_objects)

    def extract_matches(self, pages: list[PageObject]) -> list[tuple[str, int]]:
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
                    self.RATING_EXTRACTION_REGEX.format(current_index=current_index),
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
