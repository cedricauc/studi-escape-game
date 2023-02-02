import pytest

from main.forms import RegisterForm, ManageProfileForm
from main.models import User


@pytest.mark.django_db
def test_register_form_validate():
    """
    Tester le RegisterForm pour vérifier si les données saisies par l'utilisateur sont correctement validées ou non
    """

    temp_user = {
        'password': 'test-password',
        'confirmation': 'test-password',
        'email': 'testuser@testing.com',
        'first_name': 'Test',
        'last_name': 'User'
    }

    user = RegisterForm(data=temp_user)

    assert user.is_valid()


@pytest.mark.django_db
def test_register_form_save_method():
    """
    Tester si l'objet User est créé correctement en utilisant registerForm ou non
    """

    temp_user = {
        'password': 'test-password',
        'confirmation': 'test-password',
        'email': 'testuser@testing.com',
        'first_name': 'Test',
        'last_name': 'User'
    }

    form = RegisterForm(data=temp_user)
    user = form.save()

    assert isinstance(user, User)


@pytest.mark.django_db
def test_manage_profile_form_validate():
    """
    Tester le ManageProfileForm pour vérifier si les données saisies par l'utilisateur sont correctement validées ou non
    """

    temp_user = {
        'id': 1,
        'password': 'test-password',
        'confirmation': 'test-password',
        'first_name': 'Test',
        'last_name': 'User'
    }

    user = ManageProfileForm(data=temp_user)

    assert user.is_valid()


@pytest.mark.django_db
def test_manage_profile_form_save_method():
    """
    Tester si l'objet utilisateur est créé correctement en utilisant ManageProfileForm ou non
    """

    temp_user = {
        'id': 1,
        'password': 'test-password',
        'confirmation': 'test-password',
        'first_name': 'Test',
        'last_name': 'User'
    }

    form = ManageProfileForm(data=temp_user)
    user = form.save()

    assert isinstance(user, User)
