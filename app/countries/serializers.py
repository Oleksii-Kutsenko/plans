from rest_framework import serializers

from countries.models import (
    Country,
)


class CountrySerializer(serializers.ModelSerializer):
    countryeconomicfreedomindex__score = serializers.FloatField()
    countryeconomicfreedomindex__year = serializers.IntegerField()
    countrypayingtaxesindex__score = serializers.FloatField()
    countrypayingtaxesindex__year = serializers.IntegerField()

    class Meta:
        model = Country
        fields = (
            "name",
            "countryeconomicfreedomindex__score",
            "countryeconomicfreedomindex__year",
            "countrypayingtaxesindex__score",
            "countrypayingtaxesindex__year",
        )
