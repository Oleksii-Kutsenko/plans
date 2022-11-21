from django.contrib import admin

from .models import Country


class CountryAdmin(admin.ModelAdmin):
    """
    Country admin
    """
    list_display = ("name", "iso_code")
    search_fields = ("name", "iso_code")


admin.site.register(Country, CountryAdmin)
