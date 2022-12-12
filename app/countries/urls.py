from django.urls import path, include
from rest_framework import routers

from countries.views import CountryViewSet

router = routers.DefaultRouter()
router.register(r'countries', CountryViewSet, basename="country")

urlpatterns = [
    path('', include(router.urls)),
]
