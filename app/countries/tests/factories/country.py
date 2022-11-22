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

    name = factory.LazyAttribute(lambda o: pycountry.countries.get(alpha_3=o.iso_code))
    iso_code = factory.fuzzy.FuzzyChoice(choices=country_iso_codes, getter=lambda c: c[0])
