import pytest
from django.contrib.auth.models import User

from GrowVeggies.models import Veggie, Company, VeggieFamily, Seed


@pytest.fixture
def user():
    return User.objects.create_user(username='test', password='testing')

@pytest.fixture
def user2():
    return User.objects.create_user(username='test2', password='testing2')

@pytest.fixture
def veggie(user, family):
    return Veggie.objects.create(name='veggie', family=family)


@pytest.fixture
def family(user):
    return VeggieFamily.objects.create(name='Family', order='1')


@pytest.fixture
def company(user):
    return Company.objects.create(name='Company')


@pytest.fixture
def seed(user, veggie, company):
    return Seed.objects.create(owner=user, veggie=veggie, variety='variety', company=company, comment='comment')


@pytest.fixture
def seeds(user, user2, veggie, company):
    seeds1 = []
    seeds2 = []
    for x in range(5):
        seed1 = Seed.objects.create(owner=user, veggie=veggie, variety='variety', company=company, comment='comment')
        seed2 = Seed.objects.create(owner=user2, veggie=veggie, variety='variety', company=company, comment='comment')
        seeds1.append(seed1)
        seeds2.append(seed2)
    return seeds1, seeds2
