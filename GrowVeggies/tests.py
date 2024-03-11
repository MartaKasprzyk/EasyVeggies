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


@pytest.mark.django_db
def test_company_create_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('company_add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], CompanyCreateForm)

@pytest.mark.django_db
def test_seed_create_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('seed_add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], SeedCreateForm)