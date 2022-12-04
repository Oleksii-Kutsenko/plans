import datetime

from graphene_django.utils.testing import GraphQLTestCase

from accounts.tests.factories.pension_system_information import (
    PensionSystemInformationFactory,
)
from accounts.tests.factories.user import UserFactory
from investments.models import Portfolio
from investments.schema import get_personal_max_drawdown
from investments.tests.factories.portfolio import (
    PortfolioFactory,
    PortfolioBacktestDataFactory,
)


class SchemaTestCases(GraphQLTestCase):
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

        self.assertTrue(-1 <= personal_max_drawdown <= 0)

    def test_best_portfolios_by_performance_query(self) -> None:
        """
        Test best_portfolios_by_performance query
        Returns:
            None
        """
        expected_number_of_portfolios = 5
        PortfolioBacktestDataFactory.create_batch(expected_number_of_portfolios)
        self.user.birth_date = datetime.date.today()
        self.user.save()

        response = self.query(
            """
            query {
                bestPortfoliosByPerformance {
                    name,
                }
            }
            """
        )

        self.assertEqual(
            len(response.json().get("data").get("bestPortfoliosByPerformance")),
            expected_number_of_portfolios,
        )

    def test_portfolio_mutation_hide_portfolio(self) -> None:
        """
        Test portfolio mutation
        Returns:
            None
        """
        is_visible = True
        portfolio = PortfolioFactory(visible=is_visible)

        response = self.query(
            """
            mutation updatePortfolio($portfolioId: ID, $visible: Boolean){
              updatePortfolio(portfolioId: $portfolioId, visible: $visible) {
                portfolio {
                  name
                }
              }
            }
            """,
            operation_name="updatePortfolio",
            variables={"portfolioId": portfolio.id, "visible": not is_visible},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()
            .get("data")
            .get("updatePortfolio")
            .get("portfolio")
            .get("name"),
            portfolio.name,
        )
        self.assertEqual(Portfolio.objects.filter(name=portfolio.name).count(), 0)
        self.assertEqual(Portfolio.base_manager.filter(name=portfolio.name).count(), 1)
