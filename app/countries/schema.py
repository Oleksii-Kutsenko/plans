import graphene
from graphene_django import DjangoObjectType

from .models import CountryEconomicFreedomIndex


class CountryEconomicFreedomIndexType(DjangoObjectType):
    class Meta:
        model = CountryEconomicFreedomIndex
        field = ("country", "score", "year")


class Query(graphene.ObjectType):
    economic_freedom_index = graphene.List(CountryEconomicFreedomIndexType)
    economic_freedom_index_by_year = graphene.List(CountryEconomicFreedomIndexType, year=graphene.Int())

    @staticmethod
    def resolve_economic_freedom_index(root, info):
        return CountryEconomicFreedomIndex.objects.all()

    @staticmethod
    def resolve_economic_freedom_index_by_year(root, info, year):
        return CountryEconomicFreedomIndex.objects.filter(year=year).all()


schema = graphene.Schema(query=Query)
