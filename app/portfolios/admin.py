from django.contrib import admin

from portfolios.models import LazyPortfolio, Ticker, LazyPortfolioTicker


class LazyPortfolioTickerInline(admin.TabularInline):
    model = LazyPortfolioTicker
    autocomplete_fields = ("ticker",)


class LazyPortfolioAdmin(admin.ModelAdmin):
    actions = ["make_csv_files"]
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [
        LazyPortfolioTickerInline,
    ]


class TickerAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "asset_type",
    )
    search_fields = ("symbol",)
    autocomplete_fields = ("equivalents",)


class LazyPortfolioTickerAdmin(admin.ModelAdmin):
    autocomplete_fields = ("portfolio", "ticker")


admin.site.register(LazyPortfolioTicker, LazyPortfolioTickerAdmin)
admin.site.register(Ticker, TickerAdmin)
admin.site.register(LazyPortfolio, LazyPortfolioAdmin)
