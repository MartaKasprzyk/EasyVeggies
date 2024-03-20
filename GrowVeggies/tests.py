import pytest
from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client
from django.urls import reverse

from GrowVeggies.forms import SeedCreateForm, VeggieCreateForm, CompanyCreateForm, GrowVeggieCreateForm
from GrowVeggies.models import Seed, Veggie, Company, GrowVeggie, Bed, VeggieBed, Plan


def test_home_view_get():
    url = reverse('home')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_test_home_view_get_logged_user(user):
    client = Client()
    client.force_login(user)
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_veggie_create_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('veggie_add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], VeggieCreateForm)


def test_veggie_create_view_get_not_logged():
    client = Client()
    url = reverse('veggie_add')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_veggie_create_view_post_success(user, family):
    client = Client()
    client.force_login(user)
    url = reverse('veggie_add')
    data = {'name': 'veggie_name', 'family': family.pk}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert Veggie.objects.get(name='veggie_name', family=family)

@pytest.mark.django_db
def test_veggie_create_view_post_veggie_name_exists(user, veggie, family):
    client = Client()
    client.force_login(user)
    url = reverse('veggie_add')
    data = {'name': 'veggie', 'family': family.pk}
    response = client.post(url, data, follow=True)
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 200
    assert any(str(message) == 'Veggie with this name already exists.' for message in messages)


@pytest.mark.django_db
def test_company_create_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('company_add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], CompanyCreateForm)


@pytest.mark.django_db
def test_company_create_view_get_not_logged():
    client = Client()
    url = reverse('company_add')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_company_create_view_post(user):
    client = Client()
    client.force_login(user)
    url = reverse('company_add')
    data = {'name': 'Company_name'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert Company.objects.get(name='Company_name')


@pytest.mark.django_db
def test_company_create_view_post_company_name_exists(user, company):
    client = Client()
    client.force_login(user)
    url = reverse('company_add')
    data = {'name': 'Company'}
    response = client.post(url, data, follow=True)
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 200
    assert any(str(message) == 'Company with this name already exists.' for message in messages)


@pytest.mark.django_db
def test_company_create_view_post_company_name_exists_check_if_case_insensitive(user, company):
    client = Client()
    client.force_login(user)
    url = reverse('company_add')
    data = {'name': 'company'}
    response = client.post(url, data, follow=True)
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 200
    assert any(str(message) == 'Company with this name already exists.' for message in messages)


@pytest.mark.django_db
def test_seed_create_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('seed_add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], SeedCreateForm)


def test_seed_create_view_get_not_logged():
    client = Client()
    url = reverse('seed_add')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_seed_create_view_post(user, veggie, company):
    client = Client()
    client.force_login(user)
    url = reverse('seed_add')
    data = {'veggie': veggie.pk, 'variety': 'variety', 'company': company.pk, 'comment': 'comment'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert Seed.objects.get(owner=user, veggie=veggie, variety='variety', company=company, comment='comment')


@pytest.mark.django_db
def test_seed_update_view_get(user, seed, veggie, company):
    client = Client()
    client.force_login(user)
    url = reverse('seed_update', kwargs={'pk': seed.pk})
    response = client.get(url, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_seed_update_view_get_not_logged(seed):
    client = Client()
    url = reverse('seed_update', kwargs={'pk': seed.pk})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db()
def test_seed_update_view_post(seed):
    seed.name = "other_name"
    seed.save()
    seed.refresh_from_db()
    assert seed.name == 'other_name'


@pytest.mark.django_db
def test_seed_delete_view_get(seed):
    client = Client()
    client.force_login(seed.owner)
    url = reverse('seed_delete', kwargs={'pk': seed.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['seed'] == seed


@pytest.mark.django_db
def test_seed_delete_view_get_not_logged(seed):
    client = Client()
    url = reverse('seed_delete', kwargs={'pk': seed.pk})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_seed_delete_view_post(seed):
    client = Client()
    client.force_login(seed.owner)
    url = reverse('seed_delete', kwargs={'pk': seed.pk})
    data = {'delete': 'YES'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    with pytest.raises(ObjectDoesNotExist):
        Seed.objects.get(pk=seed.pk)


@pytest.mark.django_db
def test_seed_delete_view_post(seed, user2):
    client = Client()
    client.force_login(user2)
    url = reverse('seed_delete', kwargs={'pk': seed.pk})
    data = {'delete': 'YES'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 403
    assert Seed.objects.get(pk=seed.pk)


@pytest.mark.django_db
def test_seeds_list_view_get(user, seeds):
    client = Client()
    client.force_login(user)
    url = reverse('seeds')
    response = client.get(url)
    assert response.status_code == 200
    assert list(response.context['seeds']) == seeds[0]
    assert response.context['number_of_seeds'] == 3


def test_seed_list_view_get_not_logged():
    client = Client()
    url = reverse('seeds')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_seeds_list_view_get_other_user_seeds(user, seeds):
    client = Client()
    client.force_login(user)
    url = reverse('seeds')
    response = client.get(url)
    assert response.status_code == 200
    assert not list(response.context['seeds']) == seeds[1]


@pytest.mark.django_db
def test_grow_veggie_create_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('grow_veggie_add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], GrowVeggieCreateForm)


def test_grow_create_view_get_not_logged():
    client = Client()
    url = reverse('grow_veggie_add')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_grow_veggie_create_view_post(user, veggie, sun_scale, water_scale, soil_scale, month):
    client = Client()
    client.force_login(user)
    url = reverse('grow_veggie_add')
    data = {'veggie': veggie.pk,
            'sun': [sun_scale[0].pk, sun_scale[1].pk],
            'water': [water_scale[0].pk, water_scale[1].pk],
            'soil': [soil_scale[0].pk, soil_scale[1].pk],
            'sow': [month[0].pk, month[1].pk],
            'comment': 'comment'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert GrowVeggie.objects.get(owner=user, veggie=veggie,
                                  sun=(sun_scale[0].pk, soil_scale[1].pk),
                                  water=(water_scale[0].pk, water_scale[1].pk),
                                  soil=(soil_scale[0].pk, soil_scale[1].pk),
                                  sow=(month[0].pk, month[1].pk),
                                  comment='comment')


@pytest.mark.django_db
def test_grow_veggie_update_view_get(user, grow_veggie, veggie, sun_scale, water_scale, soil_scale, month):
    client = Client()
    client.force_login(user)
    url = reverse('grow_veggie_update', kwargs={'pk': grow_veggie.pk})
    response = client.get(url, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_grow_veggie_update_view_get_not_logged(grow_veggie):
    client = Client()
    url = reverse('grow_veggie_update', kwargs={'pk': grow_veggie.pk})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db()
def test_grow_veggie_update_view_post(user, grow_veggie, veggie2, sun_scale, water_scale, soil_scale, month):
    client = Client()
    client.force_login(user)
    url = reverse('grow_veggie_update', kwargs={'pk': grow_veggie.pk})
    data = {
        'veggie': veggie2.pk,
        'sun': [sun_scale[1].pk],
        'water': [water_scale[1].pk],
        'soil': [soil_scale[1].pk],
        'sow': [month[1].pk],
        'comment': 'comment2',
    }
    response = client.post(url, data, follow=True)

    grow_veggie.refresh_from_db()

    assert response.status_code == 200
    assert grow_veggie.veggie == veggie2
    assert grow_veggie.comment == 'comment2'
    assert sun_scale[1] in list(grow_veggie.sun.all())
    assert water_scale[1] in list(grow_veggie.water.all())
    assert soil_scale[1] in list(grow_veggie.soil.all())
    assert month[1] in list(grow_veggie.sow.all())


@pytest.mark.django_db
def test_grow_veggie_delete_view_get(grow_veggie):
    client = Client()
    client.force_login(grow_veggie.owner)
    url = reverse('grow_veggie_delete', kwargs={'pk': grow_veggie.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['grow_veggie'] == grow_veggie


@pytest.mark.django_db
def test_grow_veggie_delete_view_get_not_logged(grow_veggie):
    client = Client()
    url = reverse('grow_veggie_delete', kwargs={'pk': grow_veggie.pk})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_grow_veggie_delete_view_post(grow_veggie):
    client = Client()
    client.force_login(grow_veggie.owner)
    url = reverse('grow_veggie_delete', kwargs={'pk': grow_veggie.pk})
    data = {'delete': 'YES'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    with pytest.raises(ObjectDoesNotExist):
        GrowVeggie.objects.get(pk=grow_veggie.pk)


@pytest.mark.django_db
def test_grow_veggie_delete_view_post_other_user(grow_veggie, user2):
    client = Client()
    client.force_login(user2)
    url = reverse('grow_veggie_delete', kwargs={'pk': grow_veggie.pk})
    data = {'delete': 'YES'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 403


@pytest.mark.django_db
def test_grow_veggie_list_view_get(user, grow_veggies):
    client = Client()
    client.force_login(user)
    url = reverse('grow_veggies')
    response = client.get(url)
    assert response.status_code == 200
    assert list(response.context['grow_veggies']) == grow_veggies[0]
    assert response.context['number_of_conditions'] == 3


def test_grow_veggie_list_view_get_not_logged():
    client = Client()
    url = reverse('grow_veggies')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_grow_veggie_list_view_get_other_user_grow_veggies(user, grow_veggies):
    client = Client()
    client.force_login(user)
    url = reverse('grow_veggies')
    response = client.get(url)
    assert response.status_code == 200
    assert not list(response.context['grow_veggies']) == grow_veggies[1]


@pytest.mark.django_db
def test_plan_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('plan')
    response = client.get(url)
    assert response.status_code == 200


def test_plan_view_get_not_logged():
    client = Client()
    url = reverse('plan')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_plan_option1_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('plan_option1')
    response = client.get(url)
    assert response.status_code == 200


def test_plan_option1_view_get_not_logged():
    client = Client()
    url = reverse('plan_option1')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_plan_option2_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('plan_option2')
    response = client.get(url)
    assert response.status_code == 200


def test_plan_option2_view_get_not_logged():
    client = Client()
    url = reverse('plan_option2')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_plan_list_view_get(user, plans):
    client = Client()
    client.force_login(user)
    url = reverse('plan_list')
    response = client.get(url)
    assert response.status_code == 200
    assert list(response.context['plans']) == plans[0]
    assert response.context['number_of_plans'] == 3


def test_plan_list_view_get_not_logged():
    client = Client()
    url = reverse('plan_list')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_plan_option1_view_post(user, family, veggie):
    client = Client()
    client.force_login(user)
    url = reverse('plan_option1')
    data = {'beds_amount': 1,
            'bed_name': 'bed name',
            'family': family.pk,
            'veggie': veggie.pk,
            'progress': 1,
            'plan_name': 'plan name',
            'save_plan': "SAVE PLAN",
            }
    response = client.post(url, data, follow=True)
    bed_obj = Bed.objects.get(owner=user, name='bed name')
    plan_obj = Plan.objects.get(owner=user, name='plan name')
    veggie_bed_obj = VeggieBed.objects.get(veggie=veggie, bed_id=bed_obj, progress=1, plan_id=plan_obj)
    assert response.status_code == 200


@pytest.mark.django_db
def test_plan_option2_view_post(user, family, veggie):
    client = Client()
    client.force_login(user)
    url = reverse('plan_option2')
    data = {'beds_amount': 1,
            'bed_name': 'bed name',
            'family': family.pk,
            'veggie': veggie.pk,
            'progress': 1,
            'plan_name': 'plan name',
            'save_plan': "SAVE PLAN",
            }
    response = client.post(url, data, follow=True)
    bed_obj = Bed.objects.get(owner=user, name='bed name')
    plan_obj = Plan.objects.get(owner=user, name='plan name')
    veggie_bed_obj = VeggieBed.objects.get(veggie=veggie, bed_id=bed_obj, progress=1, plan_id=plan_obj)
    assert response.status_code == 200


@pytest.mark.django_db
def test_plan_details_view_get(plan):
    client = Client()
    client.force_login(plan.owner)
    url = reverse('plan_details', kwargs={'pk': plan.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['plan'] == plan


@pytest.mark.django_db
def test_plan_details_view_get_not_logged(plan):
    client = Client()
    url = reverse('plan_details', kwargs={'pk': plan.pk})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_plan_option2_choose_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('plan_option2_choose')
    response = client.get(url)
    assert response.status_code == 200


def test_plan_option2_choose_view_get_not_logged():
    client = Client()
    url = reverse('plan_option2_choose')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_plan_option2_upload_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('plan_option2_upload_plan')
    response = client.get(url)
    assert response.status_code == 200


def test_plan_option2_upload__view_get_not_logged():
    client = Client()
    url = reverse('plan_option2_upload_plan')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_plan_option2_upload_view_post(user, family, veggie, plan):
    client = Client()
    client.force_login(user)
    url = reverse('plan_option2_upload_plan')
    data = {'prev_plan': plan.pk,
            'amount': 1,
            'bed_name': 'bed name',
            'family': family.pk,
            'veggie': veggie.pk,
            'progress': 1,
            'plan_name': 'plan name',
            'save_plan': "SAVE PLAN",
            }
    response = client.post(url, data, follow=True)
    bed_obj = Bed.objects.get(owner=user, name='bed name')
    plan_obj = Plan.objects.get(owner=user, name='plan name')
    veggie_bed_obj = VeggieBed.objects.get(veggie=veggie, bed_id=bed_obj, progress=1, plan_id=plan_obj)
    assert response.status_code == 200


@pytest.mark.django_db
def test_plan_delete_view_get(plan):
    client = Client()
    client.force_login(plan.owner)
    url = reverse('plan_delete', kwargs={'pk': plan.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['plan'] == plan


@pytest.mark.django_db
def test_plan_delete_view_get_not_logged(plan):
    client = Client()
    url = reverse('plan_delete', kwargs={'pk': plan.pk})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_plan_delete_view_post(plan):
    client = Client()
    client.force_login(plan.owner)
    url = reverse('plan_delete', kwargs={'pk': plan.pk})
    data = {'delete': 'YES'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    with pytest.raises(ObjectDoesNotExist):
        Plan.objects.get(pk=plan.pk)


@pytest.mark.django_db
def test_plan_delete_view_post_other_user(plan, user2):
    client = Client()
    client.force_login(user2)
    url = reverse('plan_delete', kwargs={'pk': plan.pk})
    data = {'delete': 'YES'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 403


@pytest.mark.django_db
def test_plan_update_view_get(plan):
    client = Client()
    client.force_login(plan.owner)
    url = reverse('plan_update', kwargs={'pk': plan.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['plan'] == plan


@pytest.mark.django_db
def test_plan_update_view_get_not_logged(plan):
    client = Client()
    url = reverse('plan_update', kwargs={'pk': plan.pk})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db()
def test_plan_update_view_post(user, veggie2, plan, veggie_bed, bed, veggie):
    client = Client()
    client.force_login(user)
    url = reverse('plan_update', kwargs={'pk': plan.pk})
    data = {'plan_name': 'plan_name',
            'bed_name': 'bed_name',
            'veggie': veggie2.pk,
            'progress': 3,
            'update_plan': "UPDATE PLAN",
            'plan_veggie_beds': veggie_bed.pk,
            }
    response = client.post(url, data, follow=True)

    plan.name = 'plan_name'
    plan.save()
    plan.refresh_from_db()

    veggie_bed.bed.name = "bed_name"
    veggie_bed.veggie_id = veggie2.pk
    veggie_bed.progress = 3

    veggie_bed.bed.save()
    veggie_bed.veggie.save()
    veggie_bed.save()

    plan.refresh_from_db()
    veggie_bed.refresh_from_db()

    assert response.status_code == 200
    assert plan.name == 'plan_name'
    assert veggie_bed.bed.name == 'bed_name'
    assert veggie_bed.veggie == veggie2
    assert veggie_bed.progress == 3


@pytest.mark.django_db
def test_bed_details_view_get(user, bed):
    client = Client()
    client.force_login(user)
    url = reverse('bed_details', kwargs={'pk': bed.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_bed_details_view_get_not_logged(bed):
    client = Client()
    url = reverse('bed_details', kwargs={'pk': bed.pk})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_bed_update_view_get(user, bed):
    client = Client()
    client.force_login(user)
    url = reverse('bed_update', kwargs={'pk': bed.pk})
    response = client.get(url, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_bed_update_view_get_not_logged(bed):
    client = Client()
    url = reverse('bed_update', kwargs={'pk': bed.pk})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db()
def test_bed_update_view_post(user, bed, sun2, soil2, water2):
    client = Client()
    client.force_login(user)
    url = reverse('bed_update', kwargs={'pk': bed.pk})
    data = {
        'name': "other_bed_name",
        'sun': sun2.pk,
        'water': water2.pk,
        'soil': soil2.pk,
    }
    response = client.post(url, data, follow=True)
    bed.name = 'other_bed_name'
    bed.sun_id = sun2.pk
    bed.water_id = water2.pk
    bed.soil_id = soil2.pk
    bed.save()
    bed.sun.save()
    bed.water.save()
    bed.soil.save()
    bed.refresh_from_db()
    assert response.status_code == 200
    assert bed.name == 'other_bed_name'
    assert bed.sun == sun2
    assert bed.water == water2
    assert bed.soil == soil2


@pytest.mark.django_db
def test_bed_delete_view_get(bed):
    client = Client()
    client.force_login(bed.owner)
    url = reverse('bed_delete', kwargs={'pk': bed.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['bed'] == bed


@pytest.mark.django_db
def test_bed_delete_view_get_not_logged(bed):
    client = Client()
    url = reverse('bed_delete', kwargs={'pk': bed.pk})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_bed_delete_view_post(bed):
    client = Client()
    client.force_login(bed.owner)
    url = reverse('bed_delete', kwargs={'pk': bed.pk})
    data = {'delete': 'YES'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    with pytest.raises(ObjectDoesNotExist):
        Bed.objects.get(pk=bed.pk)


@pytest.mark.django_db
def test_bed_delete_view_post_other_user(bed, user2):
    client = Client()
    client.force_login(user2)
    url = reverse('bed_delete', kwargs={'pk': bed.pk})
    data = {'delete': 'YES'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 403

@pytest.mark.django_db
def test_filter_veggies_view_get(user, family, family2, veggie, veggie2, veggie3):
    client = Client()
    client.force_login(user)
    url = reverse('filter_veggies')
    data = {'family': family.pk}
    response = client.get(url, data)
    assert response.status_code == 200
    assert list(response.context['veggies']) == [veggie2, veggie]


@pytest.mark.django_db
def test_filter_veggies_view_get(user, family, family2, veggie, veggie2, veggie3):
    client = Client()
    client.force_login(user)
    url = reverse('filter_veggies')
    data = {'family': family.pk}
    response = client.get(url, data)
    assert response.status_code == 200
    assert not list(response.context['veggies']) == [veggie3]


@pytest.mark.django_db
def test_filter_seeds_view_get(user, seeds, veggie):
    client = Client()
    client.force_login(user)
    url = reverse('seeds')
    data = {'veggie': veggie.pk}
    response = client.get(url, data)
    assert response.status_code == 200
    assert list(response.context['seeds']) == seeds[0]
    assert not list(response.context['seeds']) == seeds[2]


@pytest.mark.django_db
def test_filter_seeds_view_get(user, seeds, company):
    client = Client()
    client.force_login(user)
    url = reverse('seeds')
    data = {'company': company.pk}
    response = client.get(url, data)
    assert response.status_code == 200
    assert list(response.context['seeds']) == seeds[0]
    assert not list(response.context['seeds']) == seeds[2]


@pytest.mark.django_db
def test_filter_seeds_view_get(user, seeds):
    client = Client()
    client.force_login(user)
    url = reverse('seeds')
    data = {'variety': 'variety2'}
    response = client.get(url, data)
    assert response.status_code == 200
    assert list(response.context['seeds']) == seeds[2]
    assert not list(response.context['seeds']) == seeds[0]


@pytest.mark.django_db
def test_filter_plans_view_get(user, plans):
    client = Client()
    client.force_login(user)
    url = reverse('plan_list')
    data = {'plan': 'name2'}
    response = client.get(url, data)
    assert response.status_code == 200
    assert list(response.context['plans']) == plans[2]
    assert not list(response.context['plans']) == plans[0]


@pytest.mark.django_db
def test_filter_grow_veggies_list_view_get(user, grow_veggies, veggie2):
    client = Client()
    client.force_login(user)
    url = reverse('grow_veggies')
    data = {'veggie': veggie2.pk}
    response = client.get(url, data)
    assert response.status_code == 200
    assert list(response.context['grow_veggies']) == grow_veggies[2]
    assert not list(response.context['grow_veggies']) == grow_veggies[0]
