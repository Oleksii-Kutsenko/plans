"""
Models for the investments' app.
"""
from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


class VisiblePortfolioManager(models.Manager):
    """
    Manager returns visible portfolios
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Get visible portfolios
        Returns:
            Queryset with visible portfolios
        """
        return super().get_queryset().filter(visible=True)


class Portfolio(models.Model):
    """
    Model that represents portfolio
    """

    base_manager = models.Manager()
    objects = VisiblePortfolioManager()

    cagr = models.FloatField(
        null=True, help_text=_("Compound annual growth rate"), blank=True
    )
    market_correlation = models.FloatField(null=True, blank=True)
    max_drawdown = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    sharpe = models.FloatField(null=True, blank=True)
    sortino = models.FloatField(null=True, blank=True)
    standard_deviation = models.FloatField(null=True, blank=True)
    visible = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def create_portfolio_tickets(
        self, portfolio_tickets: List["PortfolioTicker"]
    ) -> "Portfolio":
        """
        Creates portfolio
        Returns:
            Created portfolio
        """
        assert sum(ticker.weight for ticker in portfolio_tickets) == 100
        PortfolioTicker.objects.bulk_create(portfolio_tickets)
        return self

    def get_allocation(self) -> dict:
        """
        Returns allocation of this portfolio
        """
        return {
            ticker.ticker.symbol: float(round(ticker.weight / 100, 4))
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
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.portfolio} {self.ticker} {self.weight}"

    class Meta:
        """
        Meta class
        """

        unique_together = ("portfolio", "ticker")
