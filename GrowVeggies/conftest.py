import pytest
from django.contrib.auth.models import User

from GrowVeggies.models import Veggie, Company, VeggieFamily, Seed, GrowVeggie, SunScale, WaterScale, SoilScale, Month


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


@pytest.fixture
def sun_scale():
    scale = []
    for x in range(3):
        sun = SunScale.objects.create(name='name')
        scale.append(sun)
    return scale


@pytest.fixture
def water_scale():
    scale = []
    for x in range(2):
        water = WaterScale.objects.create(name='name')
        scale.append(water)
    return scale


@pytest.fixture
def soil_scale():
    scale = []
    for x in range(2):
        soil = SoilScale.objects.create(name='name')
        scale.append(soil)
    return scale


@pytest.fixture
def month():
    months = []
    month1 = Month.objects.create(name='name', order='1')
    month2 = Month.objects.create(name='name', order='2')
    months.append(month1)
    months.append(month2)
    return months


@pytest.fixture
def grow_veggie(user, veggie, sun_scale, water_scale, soil_scale, month):
    grow_veggie = GrowVeggie.objects.create(owner=user, veggie=veggie, comment='comment')
    grow_veggie.sun.set(sun_scale)
    grow_veggie.water.set(water_scale)
    grow_veggie.soil.set(soil_scale)
    grow_veggie.sow.set(month)
    return grow_veggie


@pytest.fixture
def grow_veggies(user, user2, veggie, sun_scale, water_scale, soil_scale, month):
    grow_veggies_list1 = []
    grow_veggies_list2 = []
    for x in range(3):
        grow_veggie_1 = GrowVeggie.objects.create(owner=user, veggie=veggie, comment='comment')
        grow_veggie_1.sun.set(sun_scale)
        grow_veggie_1.water.set(water_scale)
        grow_veggie_1.soil.set(soil_scale)
        grow_veggie_1.sow.set(month)
        grow_veggies_list1.append(grow_veggie_1)
        grow_veggie_2 = GrowVeggie.objects.create(owner=user2, veggie=veggie, comment='comment')
        grow_veggie_2.sun.set(sun_scale)
        grow_veggie_2.water.set(water_scale)
        grow_veggie_2.soil.set(soil_scale)
        grow_veggie_2.sow.set(month)
        grow_veggies_list2.append(grow_veggie_2)
    return grow_veggies_list1, grow_veggies_list2
