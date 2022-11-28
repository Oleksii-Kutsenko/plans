"""
Command that calculates import portfolios parameters
"""
import testfolio as tfs
from django.core.management import BaseCommand, CommandParser

from investments.models import Portfolio


def is_all_data_available(portfolio: Portfolio) -> bool:
    """
    Check if all parameters are available for portfolio
    Args:
        portfolio: Portfolio object

    Returns:
        bool: True if all parameters are available, False otherwise
    """
    return all(
        [
            portfolio.max_drawdown,
            portfolio.cagr,
            portfolio.standard_deviation,
            portfolio.sharpe,
            portfolio.sortino,
            portfolio.market_correlation,
        ]
    )


class Command(BaseCommand):
    """
    Management command to calculate statistics for portfolios
    """

    help = "Calculate portfolios statistics"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--force-recalculation",
            action="store_true",
            help="Force recalculation of portfolios statistics",
        )

    def handle(self, *args: list, **options: dict) -> None:
        for portfolio in Portfolio.objects.all():
            if not is_all_data_available(portfolio) or options.get(
                "force_recalculation"
            ):
                print(f"Calculating portfolio statistics for {portfolio.name}")
                backtest = tfs.Backtest(portfolio.get_allocation(), rebalance="no")
                portfolio.max_drawdown = round(backtest.max_drawdown, 4)
                portfolio.cagr = round(backtest.cagr, 4)
                portfolio.standard_deviation = round(backtest.std, 4)
                portfolio.sharpe = round(backtest.sharpe, 4)
                portfolio.sortino = round(backtest.sortino, 4)
                portfolio.market_correlation = round(backtest.correlation, 4)
                portfolio.save()
