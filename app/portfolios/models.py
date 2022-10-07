from django.db import models
from django.utils.translation import gettext_lazy as _


class LazyPortfolio(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Ticker(models.Model):
    class TickerTypes(models.TextChoices):
        BONDS = "Bonds", _("Bonds")
        COMMODITIES = "Comm", _("Commodities")
        STOCKS = "Stocks", _("Stocks")

    equivalents = models.ManyToManyField("self", blank=True)
    expense_ratio = models.FloatField()
    inception_date = models.DateField()
    portfolio = models.ManyToManyField(LazyPortfolio, through="LazyPortfolioTicker")
    symbol = models.CharField(max_length=100, unique=True)
    type = models.CharField(
        max_length=10, choices=TickerTypes.choices, default=TickerTypes.STOCKS
    )

    def __str__(self) -> str:
        return self.symbol


class LazyPortfolioTicker(models.Model):
    portfolio = models.ForeignKey(LazyPortfolio, models.CASCADE)
    ticker = models.ForeignKey(Ticker, models.CASCADE)
    weight = models.FloatField(null=False)

    def __str__(self) -> str:
        return f"{self.portfolio} {self.ticker} {self.weight}"
