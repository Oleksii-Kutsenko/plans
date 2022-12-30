import csv
from pathlib import Path
from typing import Any

import pycountry
from django.core.management.base import BaseCommand

from countries.management.commands.counties_mapping import (
    MappingSolver,
    territories_regions_unrecognized_countries,
)
from countries.models import CountryExportsValue, Country


class Command(BaseCommand):
    help = "Pulls data from WTO CSV files and saves it to the database"
    EXPORT_DATA_PATH = Path(
        "countries/management/commands/data/WtoData_20221230062725.csv"
    )

    def handle(self, *args: Any, **options: Any) -> None:
        with open(self.EXPORT_DATA_PATH, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)

            country_exports_objs = []
            for row in reader:
                if row[5] == "Reporting Economy":
                    continue
                country_name = row[5]

                country_name = MappingSolver.get_country_name(country_name)
                if country_name in territories_regions_unrecognized_countries:
                    continue

                year = row[19]
                value = row[-1]

                search_results = pycountry.countries.search_fuzzy(country_name)
                country_iso_code = search_results[0].alpha_3
                country_name = search_results[0].name

                country = Country.objects.get(
                    name=country_name, iso_code=country_iso_code
                )
                country_exports_objs.append(
                    CountryExportsValue(
                        country=country,
                        year=year,
                        value=value,
                    )
                )

        CountryExportsValue.objects.all().delete()
        CountryExportsValue.objects.bulk_create(country_exports_objs)
