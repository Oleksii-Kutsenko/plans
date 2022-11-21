from django.contrib import admin

from .models import User, PensionSystemInformation


class UserAdmin(admin.ModelAdmin):
    """
    User admin
    """
    list_display = ("email", "username", "is_staff")
    search_fields = ("email", "username")


class PensionSystemInformationAdmin(admin.ModelAdmin):
    """
    Pension system information admin
    """
    list_display = ("country",)
    search_fields = ("country",)
    autocomplete_fields = ("country",)


admin.site.register(User, UserAdmin)
admin.site.register(PensionSystemInformation, PensionSystemInformationAdmin)
