"""
Models for the investments' app.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Portfolio(models.Model):
    """
    Model that represents investments
    """

    name = models.CharField(max_length=100, unique=True)
    cagr = models.FloatField(null=True, help_text=_("Compound annual growth rate"))
    standard_deviation = models.FloatField(null=True)
    sharpe = models.FloatField(null=True)
    sortino = models.FloatField(null=True)
    market_correlation = models.FloatField(null=True)
    max_drawdown = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def get_allocation(self) -> dict:
        """
        Returns allocation of this portfolio
        """
        return {
            ticker.ticker.symbol: round(ticker.weight / 100, 4)
            for ticker in self.tickers.all()
        }


class Ticker(models.Model):
    """
    Model that represents stocks
    """

    class TickerTypes(models.TextChoices):
        """
        Ticker types
        """
        BONDS = "Bonds", _("Bonds")
        COMMODITIES = "Commodities", _("Commodities")
        REAL_ESTATE = "Real Estate", _("Real Estate")
        STOCKS = "Stocks", _("Stocks")

    equivalents = models.ManyToManyField("self", blank=True)
    expense_ratio = models.FloatField(blank=True, null=True)
    inception_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=100)
    portfolio = models.ManyToManyField(Portfolio, through="PortfolioTicker")
    symbol = models.CharField(max_length=100, unique=True)
    asset_type = models.CharField(
        max_length=15, choices=TickerTypes.choices, default=TickerTypes.STOCKS
    )

    def __str__(self) -> str:
        return f"{self.symbol}"


class PortfolioTicker(models.Model):
    """
    Helper model for M2M relationship between Tickers and Portfolios
    """

    portfolio = models.ForeignKey(Portfolio, models.PROTECT, related_name="tickers")
    ticker = models.ForeignKey(Ticker, models.PROTECT)
    weight = models.FloatField(null=False)

    def __str__(self) -> str:
        return f"{self.portfolio} {self.ticker} {self.weight}"
