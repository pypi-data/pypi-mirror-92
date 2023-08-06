import random
import string
import faker
from datetime import datetime

from django_namek import constants


class Faker(faker.Faker):
    fake = None

    def __init__(self):
        super().__init__(constants.DN_TEST_FAKER_LOCATION)
        self.add_provider(faker.providers.profile)
        self.add_provider(faker.providers.person)
        self.add_provider(faker.providers.address)
        self.add_provider(faker.providers.company)

    @property
    def rdate(self):
        return datetime(2018, 12, self.randint(24, 29)).isoformat()

    @property
    def birthday(self):
        return datetime(
            self.randint(1950, 1990),
            self.randint(1, 12),
            self.randint(1, 27)
        ).isoformat()

    @property
    def letter(self):
        return random.choice(string.ascii_letters)

    def randint(self, nb1, nb2):
        return random.randint(nb1, nb2)

    def randfloat(self, nb1, nb2):
        return random.uniform(nb1, nb2)

    def randtuple(self, tup):
        return tup[self.randint(0, len(tup) - 1)]

    def sample(self, population, k):
        return random.sample(population, k)
