"""
Command that calculates import portfolios parameters
"""
import testfolio as tfs
from django.core.management import BaseCommand, CommandParser

from investments.models import Portfolio, PortfolioBacktestData


def is_all_data_available(portfolio: Portfolio) -> bool:
    """
    Check if all parameters are available for portfolio
    Args:
        portfolio: Portfolio object

    Returns:
        bool: True if all parameters are available, False otherwise
    """
    try:
        portfolio.backtest_data
    except PortfolioBacktestData.DoesNotExist:
        return False

    backtest_data = PortfolioBacktestData.objects.filter(
        portfolio=portfolio
    ).values_list()
    return all(backtest_data[0])


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

                backtest_data = PortfolioBacktestData.objects.filter(portfolio=portfolio).first()
                if backtest_data:
                    backtest_data.delete()

                backtest_data = PortfolioBacktestData(
                    portfolio=portfolio,
                    cagr=backtest.cagr,
                    market_correlation=backtest.correlation,
                    max_drawdown=backtest.max_drawdown,
                    sharpe=backtest.sharpe,
                    sortino=backtest.sortino,
                    standard_deviation=backtest.std,
                    start_date=backtest.start_date,
                )
                backtest_data.save()
