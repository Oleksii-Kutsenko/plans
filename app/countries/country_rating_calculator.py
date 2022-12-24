import pandas as pd
from django.db.models import Q
from django.db.models import QuerySet

from countries.models import (
    CountryEconomicFreedomIndex,
    CountryPayingTaxesIndex,
    CountrySuicideRate,
    Country,
    CountryReserveCurrency,
    ReserveCurrency,
    CountryGDP,
)


class CountryRatingCalculator:
    """
    Calculate country rating based on economic freedom index, paying taxes index and suicide rate
    """

    rating_component = {
        "economic_freedom_index": {
            "orm_key": "countryeconomicfreedomindex",
            "model": CountryEconomicFreedomIndex,
            "inverted": False,
        },
        "paying_taxes_index": {
            "orm_key": "countrypayingtaxesindex",
            "model": CountryPayingTaxesIndex,
            "inverted": False,
        },
        "suicide_rate": {
            "orm_key": "countrysuiciderate",
            "model": CountrySuicideRate,
            "inverted": True,
        },
        "reserve_currency": {
            "orm_key": "reserve_currency",
            "model": CountryReserveCurrency,
            "inverted": False,
            "nested": {
                "orm_key": "reserve_currency__reserve_currency",
                "orm_key_value": "reserve_currency__reserve_currency__percentage_in_world_reserves",
                "model": ReserveCurrency,
            },
        },
        "gdp": {"orm_key": "countrygdp", "model": CountryGDP, "inverted": False},
    }

    def __init__(self) -> None:
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
        for component_setting in self.rating_component.values():
            if not component_setting.get("model"):
                raise Exception("Component setting model not set")

            if component_setting.get("nested"):
                model = component_setting["nested"].get("model")
                orm_year_key = f'{component_setting["nested"].get("orm_key")}__year'
                latest_components_years.append(
                    Q(**{orm_year_key: model.objects.latest("year").year})
                    | Q(
                        **{
                            f'{component_setting["nested"].get("orm_key")}__isnull': True
                        }
                    )
                )
            else:
                model = component_setting.get("model")
                orm_year_key = f"{component_setting.get('orm_key')}__year"
                latest_components_years.append(
                    (
                        Q(**{orm_year_key: model.objects.latest("year").year})
                        | Q(**{f'{component_setting.get("orm_key")}__isnull': True})
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
        for component_setting in self.rating_component.values():
            if component_setting.get("nested"):
                components_values_list.append(
                    component_setting["nested"].get("orm_key_value")
                )
                components_values_list.append(
                    f'{component_setting["nested"].get("orm_key")}__year'
                )
            else:
                components_values_list.append(
                    f"{component_setting.get('orm_key')}__value"
                )
                components_values_list.append(
                    f"{component_setting.get('orm_key')}__year"
                )
        return components_values_list

    def query_data(self) -> QuerySet[Country]:
        """
        Returns queryset with countries rating components scores
        Returns:
            QuerySet: queryset with countries rating components scores
        """
        prefetch_related_components = [
            value.get("orm_key") for key, value in self.rating_component.items()
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
        for component_name in self.rating_component:
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
            f"{component_name}_normalized" for component_name in self.rating_component
        ]
        for component_name, component_settings in self.rating_component.items():
            max_value = dataframe[f"{component_name}_value"].max()
            min_value = dataframe[f"{component_name}_value"].min()

            if component_settings.get("inverted"):
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
