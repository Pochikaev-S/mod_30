import random

import factory
import factory.fuzzy as fuzzy

from mod_30.src.app import db
from mod_30.src.models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.LazyAttribute(lambda x: random.randrange(0, 1))
    car_number = fuzzy.FuzzyText(prefix="№-")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = factory.LazyAttribute(lambda x: random.randrange(0, 1))
    count_places = factory.LazyAttribute(lambda x: random.randrange(5, 10))
    count_available_places = 2
