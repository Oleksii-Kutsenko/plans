from django.db import models
from django.utils.translation import gettext_lazy as _


class LazyPortfolio(models.Model):
    """
    Model that represents investments
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Ticker(models.Model):
    """
    Model that represents stocks
    """
    class TickerTypes(models.TextChoices):
        BONDS = "Bonds", _("Bonds")
        COMMODITIES = "Commodities", _("Commodities")
        REAL_ESTATE = "Real Estate", _("Real Estate")
        STOCKS = "Stocks", _("Stocks")

    equivalents = models.ManyToManyField("self", blank=True)
    expense_ratio = models.FloatField(null=True)
    inception_date = models.DateField(null=True)
    name = models.CharField(max_length=100)
    portfolio = models.ManyToManyField(LazyPortfolio, through="LazyPortfolioTicker")
    symbol = models.CharField(max_length=100, unique=True)
    asset_type = models.CharField(
        max_length=15, choices=TickerTypes.choices, default=TickerTypes.STOCKS
    )

    def __str__(self) -> str:
        return self.symbol


class LazyPortfolioTicker(models.Model):
    """
    Helper model for M2M relationship between Tickers and Portfolios
    """
    portfolio = models.ForeignKey(LazyPortfolio, models.CASCADE)
    ticker = models.ForeignKey(Ticker, models.CASCADE)
    weight = models.FloatField(null=False)

    def __str__(self) -> str:
        return f"{self.portfolio} {self.ticker} {self.weight}"
