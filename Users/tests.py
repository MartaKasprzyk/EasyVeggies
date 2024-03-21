import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


def test_register_user_view_get():
    client = Client()
    url = reverse('registration')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_user_view_post_passwords_different():
    client = Client()
    url = reverse('registration')
    data = {'username': 'test_user', 'password': 'Aaaaa1@', 'password_repeat': 'aaaaaaa'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == "Passwords are different! Please try again."


@pytest.mark.django_db
def test_register_user_view_post_success():
    client = Client()
    url = reverse('registration')
    data = {'username': 'test_user', 'password': 'Aaaaa1@', 'password_repeat': 'Aaaaa1@'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    user = User.objects.get(username="test_user")


@pytest.mark.django_db
def test_register_user_view_post_username_exists(user):
    client = Client()
    url = reverse('registration')
    data = {'username': 'test', 'password': 'Aaaaa1@', 'password_repeat': 'Aaaaa1@'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == f"This username is already taken. Please try again."


@pytest.mark.django_db
def test_register_user_view_post_password_no_big_letter():
    client = Client()
    url = reverse('registration')
    data = {'username': 'test', 'password': 'aaaaa1@', 'password_repeat': 'aaaaa1@'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == f'Weak password. Please try again.'


@pytest.mark.django_db
def test_register_user_view_post_password_no_small_letter():
    client = Client()
    url = reverse('registration')
    data = {'username': 'test', 'password': 'AAAAA1@', 'password_repeat': 'AAAAA1@'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == f'Weak password. Please try again.'


@pytest.mark.django_db
def test_register_user_view_post_password_no_number():
    client = Client()
    url = reverse('registration')
    data = {'username': 'test', 'password': 'Aaaaaa@', 'password_repeat': 'Aaaaaa@'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == f'Weak password. Please try again.'


@pytest.mark.django_db
def test_register_user_view_post_password_no_special_character():
    client = Client()
    url = reverse('registration')
    data = {'username': 'test', 'password': 'Aaaaa1a', 'password_repeat': 'Aaaaa1a'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == f'Weak password. Please try again.'


def test_login_view_get():
    client = Client()
    url = reverse("login")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_post_success(user):
    client = Client()
    url = reverse('login')
    data = {'username': user.username, 'password': 'testing'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert response.context['user'] == user


@pytest.mark.django_db
def test_login_view_post_wrong_password(user):
    client = Client()
    url = reverse('login')
    data = {'username': user.username, 'password': '12345'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert response.context['error'] == 'Login unsuccessful. Please try again.'


@pytest.mark.django_db
def test_login_view_post_wrong_password(user):
    client = Client()
    url = reverse('login')
    data = {'username': 'wrong_user', 'password': 'testing'}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert response.context['error'] == 'Login unsuccessful. Please try again.'


@pytest.mark.django_db
def test_logout_view_get(user):
    client = Client()
    client.force_login(user)
    url = reverse("logout")
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert not response.context['user'].is_authenticated



