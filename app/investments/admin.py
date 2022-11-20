"""
Investments admin
"""
from django.contrib import admin

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
    actions = ["make_csv_files"]
    list_display = ("name", "get_max_drawdown")
    search_fields = ("name",)
    inlines = [
        PortfolioTickerInline,
    ]

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
