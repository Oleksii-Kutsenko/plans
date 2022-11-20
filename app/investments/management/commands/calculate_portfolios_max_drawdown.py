import testfolio as tfs
from django.core.management import BaseCommand, CommandParser

from investments.models import Portfolio


class Command(BaseCommand):
    """
    Management command to calculate max drawdown for portfolios
    """
    help = "Calculate portfolios max drawdown"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--force-recalculation",
            action="store_true",
            help="Force recalculation of max drawdown",
        )

    def handle(self, *args: list, **options: dict) -> None:
        portfolios = Portfolio.objects.all()
        for portfolio in portfolios:
            if portfolio.max_drawdown is None or options.get("force_recalculation"):
                print(f"Calculating max drawdown for {portfolio.name}")
                backtest = tfs.Backtest(portfolio.get_allocation(), rebalance="no")
                portfolio.max_drawdown = backtest.max_drawdown
                portfolio.save()
