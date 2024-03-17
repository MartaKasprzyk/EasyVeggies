import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client
from django.urls import reverse

from GrowVeggies.forms import SeedCreateForm, VeggieCreateForm, CompanyCreateForm, GrowVeggieCreateForm
from GrowVeggies.models import Seed, Veggie, Company, GrowVeggie, Bed, VeggieBed, Plan


def test_base_view_get():
    url = reverse('home')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_test_base_view_get_logged_user(user):
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
def test_veggie_create_view_post(user, family):
    client = Client()
    client.force_login(user)
    url = reverse('veggie_add')
    data = {'name': 'veggie_name', 'family': family.pk}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert Veggie.objects.get(name='veggie_name', family=1)


# feature will not be allowed in the current version
# @pytest.mark.django_db
# def test_veggie_update_view_get(user, veggie):
#     client = Client()
#     client.force_login(user)
#     url = reverse('veggie_update', kwargs={'pk': veggie.pk})
#     response = client.get(url, follow=True)
#     assert response.status_code == 200

# feature will not be allowed in the current version
# @pytest.mark.django_db
# def test_veggie_update_view_get_not_logged(veggie):
#     client = Client()
#     url = reverse('veggie_update', kwargs={'pk': veggie.pk})
#     response = client.get(url)
#     assert response.status_code == 302


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


# feature will not be allowed in the current version
# @pytest.mark.django_db
# def test_company_update_view_get(user, company):
#     client = Client()
#     client.force_login(user)
#     url = reverse('company_update', kwargs={'pk': company.pk})
#     response = client.get(url, follow=True)
#     assert response.status_code == 200

# feature will not be allowed in the current version
# @pytest.mark.django_db
# def test_company_update_view_get_not_logged(company):
#     client = Client()
#     url = reverse('company_update', kwargs={'pk': company.pk})
#     response = client.get(url)
#     assert response.status_code == 302


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
            'sun': [sun_scale[0].pk, soil_scale[1].pk],
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
def test_grow_veggie_update_view_post(grow_veggie, veggie2):
    grow_veggie.veggie = veggie2.pk
    grow_veggie.save()
    grow_veggie.refresh_from_db()
    assert grow_veggie.veggie == veggie2.pk


@pytest.mark.django_db()
def test_grow_veggie_update_view_post(grow_veggie):
    grow_veggie.comment = 'other comment'
    grow_veggie.save()
    grow_veggie.refresh_from_db()
    assert grow_veggie.comment == 'other comment'


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
def test_plan_list_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('plan_list')
    response = client.get(url)
    assert response.status_code == 200


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
    data = {'bed': 'bed name',
            'family': family,
            'veggie': veggie,
            'progress': 1,
            'plan': 'plan name',
            }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert Bed.objects.get(owner=user, name='bed name')
    assert Plan.objects.get(owner=user, name='plan name')
    data2 = {
        'bed': Bed.objects.get(owner=user, name='bed name'),
        'plan': Plan.objects.get(owner=user, name='plan name'),
    }
    assert VeggieBed.objects.get(owner=user, veggie=veggie, bed=data2['bed'], progress=1, plan=data2['plan'])
    # TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'


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
def test_bed_update_view_post(bed):
    bed.name = 'other_name'
    bed.save()
    bed.refresh_from_db()
    assert bed.name == 'other_name'


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
def test_grow_veggie_delete_view_post_other_user(bed, user2):
    client = Client()
    client.force_login(user2)
    url = reverse('bed_delete', kwargs={'pk': bed.pk})
    data = {'delete': 'YES'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 403

