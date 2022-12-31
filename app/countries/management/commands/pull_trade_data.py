from pathlib import Path
from typing import Any

import pandas as pd
from django.core.management.base import BaseCommand

from countries.models import Country, CountryExportsValue, CountryTotalTradeValue


class Command(BaseCommand):
    """
    Base class for pulling trade data (import and export) from WTO CSV files and saving it to the
    database
    """

    TRADE_DATA_PATH = Path(
        "countries/management/commands/data/WtoData_20221231034121.csv"
    )
    EXPORT_INDICATOR_CODE = "ITS_MTV_AX"
    IMPORT_INDICATOR_CODE = "ITS_MTV_AM"

    def handle(self, *args: Any, **options: Any) -> None:
        country_codes = dict(Country.objects.values_list("iso_code", "id"))

        trade_dataframe = pd.read_csv(self.TRADE_DATA_PATH, encoding="utf-8")
        trade_dataframe = trade_dataframe.query(
            "`Reporting Economy ISO3A Code` in @country_codes.keys()"
        )
        trade_dataframe = trade_dataframe[
            ["Indicator Code", "Reporting Economy ISO3A Code", "Year", "Value"]
        ]
        trade_dataframe = trade_dataframe.rename(
            columns={"Reporting Economy ISO3A Code": "Code"}
        )

        export_dataframe = trade_dataframe[
            trade_dataframe["Indicator Code"] == self.EXPORT_INDICATOR_CODE
        ]
        total_trade_value_dataframe = trade_dataframe.groupby(["Code"]).sum(
            numeric_only=True
        )

        export_objects = []
        for row in export_dataframe.itertuples(index=False):
            export_objects.append(
                CountryExportsValue(
                    country_id=country_codes[row.Code],
                    value=row.Value,
                    year=row.Year,
                )
            )
        CountryExportsValue.objects.all().delete()
        CountryExportsValue.objects.bulk_create(export_objects)

        total_trade_value_objects = []
        for row in total_trade_value_dataframe.itertuples(index=True):
            total_trade_value_objects.append(
                CountryTotalTradeValue(
                    country_id=country_codes[row.Index],
                    value=row.Value,
                    year=row.Year,
                )
            )
        CountryTotalTradeValue.objects.all().delete()
        CountryTotalTradeValue.objects.bulk_create(total_trade_value_objects)
