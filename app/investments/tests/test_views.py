import datetime

from rest_framework.test import APITestCase

from accounts.tests.factories.pension_system_information import (
    PensionSystemInformationFactory,
)
from accounts.tests.factories.user import UserFactory
from investments.tests.factories.portfolio import PortfolioBacktestDataFactory
from investments.views import get_personal_max_drawdown


class PortfolioViewSetTestCase(APITestCase):
    """
    TestCases for investments app schema
    """

    def setUp(self) -> None:
        pension_system_information = PensionSystemInformationFactory()
        self.user = UserFactory(country=pension_system_information.country)
        self.client.force_login(self.user)

    def test_get_personal_max_drawdown(self) -> None:
        """
        Test get_personal_max_drawdown function
        Returns:
            None
        """
        PortfolioBacktestDataFactory.create_batch(5)

        personal_max_drawdown = get_personal_max_drawdown(self.user)

        self.assertTrue(-1 <= personal_max_drawdown <= 0)

        self.user.birth_date = datetime.date(
            (datetime.date.today() - datetime.timedelta(days=5 * 365)).year, 1, 1
        )
        self.user.save()

        personal_max_drawdown = get_personal_max_drawdown(self.user)

        self.assertTrue(-1 <= personal_max_drawdown <= 0)

        self.user.birth_date = datetime.date(
            (datetime.date.today() - datetime.timedelta(days=150 * 365)).year, 1, 1
        )
        self.user.save()

        personal_max_drawdown = get_personal_max_drawdown(self.user)
