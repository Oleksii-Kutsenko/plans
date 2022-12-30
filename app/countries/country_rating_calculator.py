from dataclasses import dataclass
from typing import Any, Type, Optional

import pandas as pd
from django.db import models
from django.db.models import Q
from django.db.models import QuerySet

from countries.models import (
    CountryEconomicFreedomIndex,
    CountryPayingTaxesIndex,
    CountrySuicideRate,
    Country,
    CountryReserveCurrency,
    CountryGDP,
    CountryGlobalFinancialCenterIndex,
)


@dataclass
class ComponentSetting:
    orm_key: str
    model: Type[models.Model]
    inverted: bool = False
    orm_key_value: Optional[str] = None


class RatingCalculatorSettings:
    """
    Settings for the rating calculator.
    """

    settings: dict[str, Any] = {
        "economic_freedom_index": ComponentSetting(
            orm_key="countryeconomicfreedomindex",
            model=CountryEconomicFreedomIndex,
        ),
        "paying_taxes_index": ComponentSetting(
            orm_key="countrypayingtaxesindex",
            model=CountryPayingTaxesIndex,
        ),
        "suicide_rate": ComponentSetting(
            orm_key="countrysuiciderate", model=CountrySuicideRate, inverted=True
        ),
        "reserve_currency": ComponentSetting(
            orm_key="reserve_currency__reserve_currency",
            model=CountryReserveCurrency,
            orm_key_value="reserve_currency__reserve_currency__percentage_in_world_reserves",
        ),
        "gdp": ComponentSetting(
            orm_key="countrygdp",
            model=CountryGDP,
        ),
        "financial_center_index": ComponentSetting(
            orm_key="countryglobalfinancialcenterindex",
            model=CountryGlobalFinancialCenterIndex,
        ),
    }

    def __init__(self, settings: Optional[dict] = None) -> None:
        if settings:
            self.settings = settings


class CountryRatingCalculator:
    """
    Calculate country rating based on economic freedom index, paying taxes index and suicide rate
    """

    def __init__(self) -> None:
        self.calculator_settings = RatingCalculatorSettings()
        self.queryset = self.query_data()
        self.dataframe = self.prepare_dataframe()

    def get_latest_components_years(self) -> list[Q]:
        """
        Returns dictionary with orm key for querying data by year and the latest
        available year for rating component
        Returns:
            dict[str, int]: dictionary with orm key and the latest available year for
                            rating component
        """
        latest_components_years = []
        for component_setting in self.calculator_settings.settings.values():
            model = component_setting.model
            orm_year_key = f"{component_setting.orm_key}__year"
            latest_components_years.append(
                (
                    Q(**{orm_year_key: model.get_latest_available_data_year()})
                    | Q(**{f"{component_setting.orm_key}__isnull": True})
                )
            )

        return latest_components_years

    def get_components_values_list(self) -> list[str]:
        """
        Returns list of values to be used in queryset.values_list()
        Returns:
            list[str]: list of values to be used in queryset.values_list()
        """
        components_values_list = ["name"]
        for component_setting in self.calculator_settings.settings.values():
            if component_setting.orm_key_value:
                components_values_list.append(component_setting.orm_key_value)
            else:
                components_values_list.append(f"{component_setting.orm_key}__value")
            components_values_list.append(f"{component_setting.orm_key}__year")
        return components_values_list

    def query_data(self) -> QuerySet[Country]:
        """
        Returns queryset with countries rating components scores
        Returns:
            QuerySet: queryset with countries rating components scores
        """
        prefetch_related_components = [
            component_settings.orm_key
            for _, component_settings in self.calculator_settings.settings.items()
        ]
        latest_components_years = self.get_latest_components_years()
        components_values_list = self.get_components_values_list()
        queryset = (
            Country.objects.prefetch_related(*prefetch_related_components)
            .filter(*latest_components_years)
            .values_list(*components_values_list)
        )

        return queryset

    def prepare_dataframe_columns(self) -> list[str]:
        """
        Returns dataframe columns
        Returns:
            list[str]: list of dataframe columns
        """
        dataframe_columns = ["name"]
        for component_name in self.calculator_settings.settings.keys():
            dataframe_columns.append(f"{component_name}_value")
            dataframe_columns.append(f"{component_name}_year")
        return dataframe_columns

    def prepare_dataframe(self) -> pd.DataFrame:
        """
        Returns dataframe with normalized countries rating components scores and total rating

        Returns:
            pd.DataFrame: dataframe with normalized countries rating components scores and
                          total rating
        """
        dataframe = pd.DataFrame.from_records(
            self.queryset, columns=self.prepare_dataframe_columns()
        )
        normalized_columns = [
            f"{component_name}_normalized"
            for component_name in self.calculator_settings.settings.keys()
        ]
        for (
            component_name,
            component_settings,
        ) in self.calculator_settings.settings.items():
            max_value = dataframe[f"{component_name}_value"].max()
            min_value = dataframe[f"{component_name}_value"].min()

            if component_settings.inverted:
                dataframe[f"{component_name}_normalized"] = (
                    100
                    - (dataframe[f"{component_name}_value"] - min_value)
                    / (max_value - min_value)
                    * 100
                )
            else:
                dataframe[f"{component_name}_normalized"] = (
                    (dataframe[f"{component_name}_value"] - min_value)
                    / (max_value - min_value)
                    * 100
                )

            dataframe[f"{component_name}_value"].fillna("N/A", inplace=True)
            dataframe[f"{component_name}_year"].fillna("N/A", inplace=True)
            dataframe[f"{component_name}_normalized"].fillna(-100, inplace=True)

        dataframe["rating"] = dataframe[normalized_columns].mean(axis=1)
        dataframe.sort_values(by="rating", ascending=False, inplace=True)

        dataframe = dataframe.round(2)

        return dataframe
