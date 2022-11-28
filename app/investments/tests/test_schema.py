import datetime

from graphene_django.utils.testing import GraphQLTestCase

from accounts.tests.factories.pension_system_information import (
    PensionSystemInformationFactory,
)
from accounts.tests.factories.user import UserFactory
from investments.schema import get_personal_max_drawdown


class SchemaTestCases(GraphQLTestCase):
    """
    TestCases for investments app schema
    """

    fixtures = ["investments/tests/investments_fixtures.json"]

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

        self.assertTrue(-1 <= personal_max_drawdown <= 0)

    def test_best_portfolios_by_performance_query(self) -> None:
        """
        Test best_portfolios_by_performance query
        Returns:
            None
        """
        expected_number_of_portfolios = 5
        self.user.birth_date = datetime.date(
            (datetime.date.today() - datetime.timedelta(days=18 * 365)).year, 1, 1
        )
        self.user.save()

        response = self.query(
            """
            query {
                bestPortfoliosByPerformance {
                    name,
                    cagr,
                    maxDrawdown,
                }
            }
            """
        )

        self.assertEqual(
            len(response.json().get("data").get("bestPortfoliosByPerformance")),
            expected_number_of_portfolios,
        )
