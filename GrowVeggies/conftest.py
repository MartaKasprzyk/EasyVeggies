import pytest
from django.contrib.auth.models import User

from GrowVeggies.models import Veggie, Company, VeggieFamily


@pytest.fixture
def user():
    return User.objects.create_user(username='test', password='testing')


@pytest.fixture
def veggie(user, family):
    return Veggie.objects.create(name='veggie', family=family)


@pytest.fixture
def family(user):
    return VeggieFamily.objects.create(name='Family', order='1')

@pytest.fixture
def company(user):
    return Company.objects.create(name='Company')



