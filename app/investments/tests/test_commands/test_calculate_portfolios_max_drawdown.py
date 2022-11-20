from typing import List, Any
from unittest.mock import patch, MagicMock

from django.core.management import call_command
from django.test import TestCase

from ..factories.portfolio import PortfolioTickerFactory, PortfolioFactory


class CalculatePortfoliosMaxDrawdownCommandTests(TestCase):
    @patch(
        "investments.management.commands.calculate_portfolios_max_drawdown.tfs.Backtest"
    )
    def test_calculate_portfolios_max_drawdown(self, mock_backtest: MagicMock) -> None:
        """
        Test that the max drawdown is calculated correctly
        """
        max_drawdown = 0.1
        mock_backtest.return_value.max_drawdown = max_drawdown
        portfolio = PortfolioFactory()
        PortfolioTickerFactory.create_batch(4, portfolio=portfolio, weight=25)

        args: List[Any] = []
        opts = {"force_recalculation": True}
        call_command("calculate_portfolios_max_drawdown", *args, **opts)
        portfolio.refresh_from_db()

        mock_backtest.assert_called_once_with(
            portfolio.get_allocation(), rebalance="no"
        )
        assert portfolio.max_drawdown == max_drawdown
