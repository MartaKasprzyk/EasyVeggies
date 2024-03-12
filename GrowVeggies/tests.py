import pytest
from django.test import Client
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from GrowVeggies.forms import SeedCreateForm, VeggieCreateForm, CompanyCreateForm
from GrowVeggies.models import Seed, Veggie, Company


def test_base_view_get():
    url = reverse('base')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_test_base_view_get_logged_user(user):
    client = Client()
    client.force_login(user)
    url = reverse('base')
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


@pytest.mark.django_db
def test_veggie_create_view_post(user, family):
    client = Client()
    client.force_login(user)
    url = reverse('veggie_add')
    data = {'name': 'veggie_name', 'family': family.pk}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert Veggie.objects.get(name='veggie_name', family=1)


@pytest.mark.django_db
def test_veggie_update_view_get(user, veggie):
    client = Client()
    client.force_login(user)
    url = reverse('veggie_update', kwargs={'pk': veggie.pk})
    response = client.get(url, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_company_create_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('company_add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], CompanyCreateForm)


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
def test_company_update_view_get(user, company):
    client = Client()
    client.force_login(user)
    url = reverse('company_update', kwargs={'pk': company.pk})
    response = client.get(url, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_seed_create_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('seed_add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], SeedCreateForm)


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
def test_seed_delete_view_get(seed):
    client = Client()
    client.force_login(seed.owner)
    url = reverse('seed_delete', kwargs={'pk': seed.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['seed'] == seed


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


@pytest.mark.django_db
def test_seeds_list_view_get_other_user_seeds(user, seeds):
    client = Client()
    client.force_login(user)
    url = reverse('seeds')
    response = client.get(url)
    assert response.status_code == 200
    assert not list(response.context['seeds']) == seeds[1]
