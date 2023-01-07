from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from accounts.views import RegisterView

accounts_router = DefaultRouter()

urlpatterns = accounts_router.urls + [
    path("accounts/", include("rest_framework.urls")),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/token", obtain_auth_token, name="token"),
]
