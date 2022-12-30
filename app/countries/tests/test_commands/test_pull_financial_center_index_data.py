import re
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
        pages = Command.get_pages()
        expected_rating_total = 0
        current_index = 1
        for page in pages:
            text = page.extract_text()
            for line in text.split("\n"):
                match = re.search(
                    Command.RATING_EXTRACTION_REGEX.format(current_index=current_index),
                    line,
                )
                if match:
                    matched_string = match.group()
                    _, raw_rating = matched_string.split(f" {current_index} ")
                    expected_rating_total += int(raw_rating.strip())
                    current_index += 1

        call_command("pull_financial_center_index_data")

        self.assertEqual(
            CountryGlobalFinancialCenterIndex.objects.aggregate(Sum("value")).get(
                "value__sum"
            ),
            expected_rating_total,
        )
