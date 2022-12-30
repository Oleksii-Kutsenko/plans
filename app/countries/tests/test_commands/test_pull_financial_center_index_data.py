from unittest import TestCase

from django.core.management import call_command
from django.db.models import Sum

from countries.management.commands.pull_financial_center_index_data import Command
from countries.models import CountryGlobalFinancialCenterIndex


class PullFinancialCenterIndexDataTests(TestCase):
    def test_pull_financial_center_index_data_command(self) -> None:
        """
        Test pull_financial_center_index_data command
        Returns:
            None
        """
        expected_rating_total = 0
        pages = Command.get_pages()
        matches = Command.extract_matches(pages)
        countries_rating = Command.replace_cities_with_countries(matches)
        for _, _, rating in countries_rating:
            expected_rating_total += rating

        call_command("pull_financial_center_index_data")

        self.assertEqual(
            CountryGlobalFinancialCenterIndex.objects.aggregate(Sum("value")).get(
                "value__sum"
            ),
            expected_rating_total,
        )
