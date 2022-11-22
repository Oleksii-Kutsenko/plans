from typing import List, Any
from unittest.mock import patch, MagicMock

from django.core.management import call_command
from django.test import TestCase

from ..factories.portfolio import PortfolioTickerFactory, PortfolioFactory


class CalculatePortfoliosMaxDrawdownCommandTests(TestCase):
    @patch(
        "investments.management.commands.calculate_portfolios_statistics.tfs.Backtest"
    )
    def test_calculate_portfolios_max_drawdown(self, mock_backtest: MagicMock) -> None:
        """
        Test that the max drawdown is calculated correctly
        """
        backtest = MagicMock()
        backtest.max_drawdown = -0.1
        backtest.cagr = 0.2
        backtest.std = 0.3
        backtest.sharpe = 0.4
        backtest.sortino = 0.5
        backtest.correlation = 0.6
        mock_backtest.return_value = backtest
        portfolio = PortfolioFactory()
        PortfolioTickerFactory.create_batch(4, portfolio=portfolio, weight=25)

        args: List[Any] = []
        opts = {"force_recalculation": True}
        call_command("calculate_portfolios_statistics", *args, **opts)
        portfolio.refresh_from_db()

        mock_backtest.assert_called_once_with(
            portfolio.get_allocation(), rebalance="no"
        )
        assert portfolio.max_drawdown == backtest.max_drawdown
