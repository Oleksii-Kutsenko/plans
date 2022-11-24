from unittest import TestCase

from django.core.management import call_command

from accounts.models import User
from accounts.tests.factories.pension_system_information import (
    PensionSystemInformationFactory,
)
from accounts.tests.factories.user import UserFactory
from investments.models import PortfolioTicker, Portfolio
from investments.schema import get_personal_max_drawdown


class SchemaTestCases(TestCase):
    def setUp(self) -> None:
        Portfolio.objects.all().delete()
        User.objects.all().delete()

    def test_get_personal_max_drawdown(self) -> None:
        pension_system_information = PensionSystemInformationFactory()
        user = UserFactory(country=pension_system_information.country)
        call_command("pull_lazyportfolioetf_com", limit=10)
        call_command("calculate_portfolios_statistics", force_recalculation=True)

        personal_max_drawdown = get_personal_max_drawdown(user)

        self.assertGreater(personal_max_drawdown, -1)
        self.assertLess(personal_max_drawdown, 0)

    def tearDown(self) -> None:
        PortfolioTicker.objects.all().delete()
