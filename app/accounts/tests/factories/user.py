import datetime

import factory.fuzzy

from accounts.models import User
from countries.tests.factories.country import CountryFactory


class UserFactory(factory.DjangoModelFactory):
    birth_date = factory.fuzzy.FuzzyDate(
        start_date=datetime.date.today() - datetime.timedelta(days=100 * 365),
        end_date=datetime.date.today() - datetime.timedelta(days=18 * 365),
    )
    country = factory.SubFactory(CountryFactory)
    email = factory.Faker("email")
    gender = factory.fuzzy.FuzzyChoice(choices=User.GenderTypes)
    username = factory.Sequence(lambda n: f"user {n}")

    class Meta:
        model = User
