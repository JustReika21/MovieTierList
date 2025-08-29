import pytest

from rest_framework.test import APIClient


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(
        username='testuser1',
        password='password',
        email='test@gmail.com'
    )


@pytest.fixture
def user_2(django_user_model):
    return django_user_model.objects.create(
        username='testuser2',
        password='password',
        email='test2@gmail.com'
    )


@pytest.fixture
def auth_user_client(user):
    client = APIClient()
    client.force_login(user)

    return client


@pytest.fixture
def auth_user_client_2(user_2):
    client = APIClient()
    client.force_login(user_2)

    return client


@pytest.fixture
def client():
    return APIClient()