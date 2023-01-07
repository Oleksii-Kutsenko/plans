from rest_framework import routers

from investments.views import PortfolioViewSet

investments_router = routers.DefaultRouter()
investments_router.register(r"portfolios", PortfolioViewSet, basename="portfolio")

urlpatterns = investments_router.urls
