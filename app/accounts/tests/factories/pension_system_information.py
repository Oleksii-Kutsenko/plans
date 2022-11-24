import factory.fuzzy

from accounts.models import PensionSystemInformation
from countries.tests.factories.country import CountryFactory


class PensionSystemInformationFactory(factory.DjangoModelFactory):
    country = factory.SubFactory(CountryFactory)
    male_life_expectancy = factory.fuzzy.FuzzyFloat(50, 80)
    female_life_expectancy = factory.fuzzy.FuzzyFloat(55, 90)
    male_pension_age = factory.fuzzy.FuzzyFloat(55, 70)
    female_pension_age = factory.fuzzy.FuzzyFloat(55, 70)

    class Meta:
        model = PensionSystemInformation
