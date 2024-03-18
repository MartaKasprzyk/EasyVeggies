import pytest
from django.contrib.auth.models import User

from GrowVeggies.models import Veggie, Company, VeggieFamily, Seed, GrowVeggie
from GrowVeggies.models import SunScale, WaterScale, SoilScale, Month, Bed, Plan, VeggieBed


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
def veggie2(user, family):
    return Veggie.objects.create(name='other_veggie', family=family)

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
    for i in range(5):
        seed1 = Seed.objects.create(owner=user, veggie=veggie, variety='variety', company=company, comment='comment')
        seed2 = Seed.objects.create(owner=user2, veggie=veggie, variety='variety', company=company, comment='comment')
        seeds1.append(seed1)
        seeds2.append(seed2)
    return seeds1, seeds2


@pytest.fixture
def sun_scale():
    scale = []
    for i in range(3):
        the_sun = SunScale.objects.create(name='name')
        scale.append(the_sun)
    return scale


@pytest.fixture
def water_scale():
    scale = []
    for i in range(2):
        the_water = WaterScale.objects.create(name='name')
        scale.append(the_water)
    return scale


@pytest.fixture
def soil_scale():
    scale = []
    for i in range(2):
        the_soil = SoilScale.objects.create(name='name')
        scale.append(the_soil)
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
    for i in range(3):
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


@pytest.fixture
def sun():
    sun = SunScale.objects.create(name='name')
    return sun


@pytest.fixture
def water():
    water = WaterScale.objects.create(name='name')
    return water


@pytest.fixture
def soil():
    soil = SoilScale.objects.create(name='name')
    return soil


@pytest.fixture
def sun2():
    sun2 = SunScale.objects.create(name='other_name')
    return sun2


@pytest.fixture
def water2():
    water2 = WaterScale.objects.create(name='other_name')
    return water2


@pytest.fixture
def soil2():
    soil2 = SoilScale.objects.create(name='other_name')
    return soil2


@pytest.fixture
def bed(user, sun, water, soil):
    bed = Bed.objects.create(owner=user, name='name', sun=sun, water=water, soil=soil)
    return bed


@pytest.fixture
def veggie_bed(veggie, bed, plan):
    veggie_bed = VeggieBed.objects.create(veggie=veggie, bed=bed, progress=1, plan=plan)
    return veggie_bed


@pytest.fixture
def plan(user):
    plan = Plan.objects.create(owner=user, name='name')
    return plan

@pytest.fixture
def plans(user, user2):
    plans_user = []
    plans_user2 = []
    for i in range(3):
        plan_1 = Plan.objects.create(owner=user, name='name')
        plan_2 = Plan.objects.create(owner=user2, name='name2')
        plans_user.append(plan_1)
        plans_user2.append(plan_2)
    return plans_user, plans_user2



