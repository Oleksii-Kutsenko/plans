from rest_framework import serializers

from countries.models import (
    Country,
)


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer for the Country model
    """

    class Meta:
        model = Country
        fields = ("name",)
