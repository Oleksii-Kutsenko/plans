"""
Investments admin
"""
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

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
    list_display = ("name", "get_max_drawdown")
    search_fields = ("name",)
    inlines = [
        PortfolioTickerInline,
    ]

    def get_queryset(self, request: WSGIRequest) -> QuerySet:
        return Portfolio.base_manager.all()

    @admin.display(description="Max Drawdown", ordering="max_drawdown")
    def get_max_drawdown(self, obj: Portfolio) -> str:
        """
        Transform max drawdown for portfolio into percentage format
        Args:
            obj: Portfolio object

        Returns:
            str: Max drawdown in percentage format
        """
        return f"{round(obj.max_drawdown * 100, 2)}%" if obj.max_drawdown else "N/A"


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
