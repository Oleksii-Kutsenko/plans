import testfolio as tfs
from django.core.management import BaseCommand, CommandParser

from investments.models import Portfolio


def is_all_data_available(portfolio: Portfolio) -> bool:
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
            if is_all_data_available(portfolio) or options.get("force_recalculation"):
                print(f"Calculating portfolio statistics for {portfolio.name}")
                backtest = tfs.Backtest(portfolio.get_allocation(), rebalance="no")
                portfolio.max_drawdown = backtest.max_drawdown
                portfolio.cagr = backtest.cagr
                portfolio.standard_deviation = backtest.std
                portfolio.sharpe = backtest.sharpe
                portfolio.sortino = backtest.sortino
                portfolio.market_correlation = backtest.correlation
                portfolio.save()
