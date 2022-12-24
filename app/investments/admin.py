"""
Investments admin
"""
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Portfolio, Ticker, PortfolioTicker


class PortfolioTickerInline(admin.TabularInline):
    """
    PortfolioTicker inline for portfolio creation
    """

    model = PortfolioTicker
    autocomplete_fields = ("ticker",)


class PortfolioAdmin(admin.ModelAdmin):
    """
    Portfolio admin
    """

    fields = ("name", "visible")
    list_display = ("name", "visible", "get_max_drawdown")
    search_fields = ("name",)
    inlines = [
        PortfolioTickerInline,
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return Portfolio.base_manager.select_related("backtest_data")

    @admin.display(description="Max Drawdown", ordering="backtest_data__max_drawdown")
    def get_max_drawdown(self, obj: Portfolio) -> str:
        """
        Transform max drawdown for portfolio into percentage format
        Args:
            obj: Portfolio object

        Returns:
            str: Max drawdown in percentage format
        """
        return (
            f"{round(obj.backtest_data.max_drawdown * 100, 2)}%"
            if obj.backtest_data.max_drawdown
            else "N/A"
        )


class TickerAdmin(admin.ModelAdmin):
    """
    Ticker admin
    """

    list_display = (
        "symbol",
        "asset_type",
    )
    search_fields = ("symbol",)
    autocomplete_fields = ("equivalents",)


class PortfolioTickerAdmin(admin.ModelAdmin):
    """
    PortfolioTicker admin
    """

    autocomplete_fields = ("portfolio", "ticker")


admin.site.register(PortfolioTicker, PortfolioTickerAdmin)
admin.site.register(Ticker, TickerAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
