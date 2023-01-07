from rest_framework import routers

from countries.views import CountryViewSet

countries_router = routers.DefaultRouter()
countries_router.register(r"countries", CountryViewSet, basename="country")

urlpatterns = countries_router.urls
