"""plans URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from graphene_django.views import GraphQLView

from .schema import schema


class PrivateGraphQLView(GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/admin/login/?next=/graphql/')
        return super().dispatch(request, *args, **kwargs)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", PrivateGraphQLView.as_view(graphiql=True, schema=schema)),
    path("api/", include("countries.urls")),
]

urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
