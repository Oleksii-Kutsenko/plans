import factory.fuzzy
import pycountry

from ...models import Country, country_iso_codes


class CountryFactory(factory.django.DjangoModelFactory):
    """
    Country factory
    """

    class Meta:
        """
        Meta class
        """

        model = Country
        django_get_or_create = ("iso_code", "name")

    name = factory.LazyAttribute(
        lambda o: pycountry.countries.get(alpha_3=o.iso_code).name
    )
    iso_code = factory.fuzzy.FuzzyChoice(
        choices=country_iso_codes, getter=lambda c: c[0]
    )
