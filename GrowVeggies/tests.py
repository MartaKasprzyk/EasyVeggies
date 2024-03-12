import pytest
from django.test import Client
from django.urls import reverse

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


@pytest.mark.run(after='test_seed_create_view_post')
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
def test_company_create_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('company_add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], CompanyCreateForm)


@pytest.mark.run(after='test_veggie_create_view_post')
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
def test_seed_create_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('seed_add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], SeedCreateForm)


@pytest.mark.run(order=1)
@pytest.mark.django_db
def test_seed_create_view_post(user, veggie, company):
    client = Client()
    client.force_login(user)
    url = reverse('seed_add')
    data = {'veggie': veggie.pk, 'variety': 'variety', 'company': company.pk, 'comment': 'comment'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert Seed.objects.get(owner=user, veggie=1, variety='variety', company=1, comment='comment')
    # if running single test: veggie,company=1; if running all tests veggie,company=2; preserved info about prev created objs?
