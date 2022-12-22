from pathlib import Path
from typing import Any

import pandas as pd
import pycountry
from django.core.management import BaseCommand

from countries.models import Country, CountryReserveCurrency, ReserveCurrency

countries_usd_users = (
    "USA",
    "TLS",
    "SLV",
    "FSM",
    "PAN",
    "KHM",
    "ECU",
    "MHL",
    "PLW",
    "ZWE",
)
countries_euro_user = (
    "AUT",
    "BEL",
    "CYP",
    "EST",
    "FIN",
    "FRA",
    "DEU",
    "GRC",
    "IRL",
    "ITA",
    "LVA",
    "LTU",
    "LUX",
    "MLT",
    "NLD",
    "PRT",
    "SVK",
    "SVN",
    "ESP",
)
countries_renminbi_users = ("CHN",)
countries_yen_users = ("JPN",)
countries_pound_users = ("GBR",)
countries_aud_users = ("AUS", "KIR", "TUV", "NRU")
countries_cad_users = ("CAN",)
countries_franc_users = ("CHE", "LIE")
reserve_currency_countries_mapper = {
    "USD": countries_usd_users,
    "EUR": countries_euro_user,
    "CNY": countries_renminbi_users,
    "JPY": countries_yen_users,
    "GBP": countries_pound_users,
    "AUD": countries_aud_users,
    "CAD": countries_cad_users,
    "CHF": countries_franc_users,
}


class Command(BaseCommand):
    """
    Pull reserves currencies allocation from the Excel file
    """

    help = "Pull reserve currencies from the Excel file"
    RESERVE_CURRENCIES_DATA_YEAR = 2022
    RESERVE_CURRENCIES_DATA_PATH = Path(
        "countries/management/commands/data/reserve_currencies.xlsx"
    )

    dataframe_currencies_mapper = {
        "Claims in U.S. dollars": "USD",
        "Claims in euro": "EUR",
        "Claims in Chinese renminbi": "CNY",
        "Claims in Japanese yen": "JPY",
        "Claims in pounds sterling": "GBP",
        "Claims in Australian dollars": "AUD",
        "Claims in Canadian dollars": "CAD",
        "Claims in Swiss francs": "CHF",
    }

    def handle(self, *args: Any, **options: Any) -> None:
        currencies_dataframe = pd.read_excel(
            self.RESERVE_CURRENCIES_DATA_PATH, header=None
        )

        reserve_currencies_sum = currencies_dataframe[1].sum()
        currencies_dataframe["percentage"] = (
            currencies_dataframe[1] / reserve_currencies_sum
        )
        currencies_dataframe["currency"] = currencies_dataframe[0].map(
            self.dataframe_currencies_mapper
        )

        CountryReserveCurrency.objects.all().delete()
        ReserveCurrency.objects.all().delete()
        for (
            reserve_currency_symbol,
            countries,
        ) in reserve_currency_countries_mapper.items():
            percentage_in_world_reserves_row = currencies_dataframe.query(
                f"currency == '{reserve_currency_symbol}'"
            )

            currency, _ = ReserveCurrency.objects.get_or_create(
                symbol=reserve_currency_symbol,
                percentage_in_world_reserves=float(
                    percentage_in_world_reserves_row["percentage"]
                ),
                year=self.RESERVE_CURRENCIES_DATA_YEAR,
            )
            for country in countries:
                search_result = pycountry.countries.get(alpha_3=country)
                country, _ = Country.objects.get_or_create(
                    iso_code=search_result.alpha_3, name=search_result.name
                )
                CountryReserveCurrency.objects.create(
                    country=country,
                    reserve_currency=currency,
                )
