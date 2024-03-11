import pytest
from django.contrib.auth.models import User

from GrowVeggies.models import Seed, Veggie, Company


@pytest.fixture
def user():
    return User.objects.create_user(username='test', password='testing')