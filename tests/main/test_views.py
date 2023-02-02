from django.test import Client
from django.urls import reverse, resolve

import pytest
from pytest_django.asserts import assertTemplateUsed

client = Client()


@pytest.mark.django_db
def test_RegisterView():
    """
    In the first assert, we are checing if a user is created successfully then, the user is redirected to '/login/' route,
    For the second assert, we are checking the 302 status code(redirect)
    """

    credentials = {
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'TestUser',
        'email': 'testuser@testing.com',
        'password1': 'TestPassword',
        'password2': 'TestPassword'
    }
    response = client.post('/user/signup/', credentials)

    assert response.url == '/user/login/'
    assert response.status_code == 302
