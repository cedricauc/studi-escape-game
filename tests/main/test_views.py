import secrets

import pytest
from django.contrib import auth
from django.test import Client
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed

from main.models import User, Scenario, TicketCategory, Game

client = Client()


@pytest.mark.django_db
def test_HomeView():
    response = client.get(reverse('home'))

    """ 
    Dans la première assertion, nous testons si notre requête get renvoie le code d'état 200 (OK)
    Pour la deuxième assertion, nous nous assurons que notre vue renvoie le modèle home.html
    """

    assert response.status_code == 200
    assertTemplateUsed(response, 'main/index.html')


@pytest.mark.django_db
def test_RegisterView():
    """
    In the first assert, we are checing if a user is created successfully then, the user is redirected to '/login/' route,
    For the second assert, we are checking the 302 status code(redirect)
    """

    credentials = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testuser@testing.com',
        'password': 'TestPassword',
        'confirmation': 'TestPassword',
    }
    response = client.post(reverse('register'), credentials)

    assert response.url == reverse('home')
    assert response.status_code == 302


@pytest.mark.django_db
def test_LoginView():
    """
    Dans la première assertion, nous vérifions si un utilisateur est créé avec succès, puis l'utilisateur est redirigé vers la route '/login/',
    Pour la deuxième assertion, nous vérifions le code d'état 302 (redirection)
    """
    # Inscrire un utilisateur à l’aide de la vue `signup`afin de l’enregistrer dans la base de données
    credentials = {
        'first_name': 'test',
        'last_name': 'test',
        'username': 'test@testing.com',
        'email': 'test@testing.com',
        'password': 'TestPassword',
        'confirmation': 'TestPassword'
    }
    response = client.post(reverse('register'), credentials)

    credentials = {
        'username': 'TestUser',
        'password': 'TestPassword',
        'next': 'None'
    }
    response = client.post(reverse('login_view'), credentials)

    # Vérifier que la redirection vers la page d’accueil est effectuée
    assert response.status_code == 200

    # Vérifier que l’utilisateur est bien authentifié
    user = auth.get_user(client)
    assert user.is_authenticated


@pytest.mark.django_db
def test_LogoutView():
    """
    Tester si notre LogoutView déconnecte correctement l'utilisateur, Dans la première assertion, nous vérifions si l'utilisateur est redirigé vers
    route d'accueil, pour la deuxième affirmation, nous vérifions le code d'état de redirection 302
    """

    response = client.get(reverse('logout'))

    assert response.url == reverse('home')
    assert response.status_code == 302


@pytest.mark.django_db
def test_ManageProfileView():
    """
    Tester si ManageProfileView est rendu correctement en vérifiant le code d'état 200,
    Pour la deuxième assertion, nous nous assurons que le modèle 'profile.html' est rendu
    """

    # Authentifier un user
    my_admin = User.objects.create_user('test', 'test@test.com', 'test')
    client.login(username=my_admin.username, password='test')

    response = client.get(reverse('profile'))

    assert response.status_code == 200
    assertTemplateUsed(response, 'main/profile.html')


@pytest.mark.django_db
def test_ManageOrderView():
    """
    Vérifier si notre 'ManageOrderView' renvoie le modèle 'order.html' pour afficher le formulaire de mise à jour,
    pour la deuxième assertion, nous nous assurons que tout s'est bien passé en vérifiant le code d'état 200
    """

    # Authentifier un user
    my_admin = User.objects.create_user('test', 'test@test.com', 'test')
    client.login(username=my_admin.username, password='test')

    response = client.get(reverse('order'))

    assertTemplateUsed(response, 'main/order.html')
    assert response.status_code == 200


@pytest.mark.django_db
def test_ManageChatView():
    """
    Vérifier si notre 'ManageChatView' renvoie le modèle 'chat.html' pour afficher le formulaire de mise à jour,
    pour la deuxième assertion, nous nous assurons que tout s'est bien passé en vérifiant le code d'état 200
    """

    # Authentifier un user
    my_admin = User.objects.create_user('test', 'test@test.com', 'test')
    client.login(username=my_admin.username, password='test')

    response = client.get(reverse('chat'))

    assertTemplateUsed(response, 'main/chat.html')
    assert response.status_code == 200


@pytest.mark.django_db
def test_ScenarioView():
    """
    Vérifier si notre 'ScenarioView' renvoie le modèle 'scenario.html' pour afficher le formulaire de mise à jour,
    pour la deuxième assertion, nous nous assurons que tout s'est bien passé en vérifiant le code d'état 200
    """
    # Enregistrer un scénario
    temp_scenario = Scenario.objects.create(
        title=secrets.token_hex(5),
        description=secrets.token_hex(100),
        duration=2.5,
        min_participant=2,
        max_participant=9,
        price_participant=20.5,
        slug=secrets.token_hex(5), )

    response = client.get(reverse('scenario', args=[temp_scenario.slug]))

    assertTemplateUsed(response, 'main/scenario.html')
    assert response.status_code == 200


@pytest.mark.django_db
def test_FaqView():
    """
    Vérifier si notre 'FaqView' renvoie le modèle 'scenario.html' pour afficher le formulaire de mise à jour,
    pour la deuxième assertion, nous nous assurons que tout s'est bien passé en vérifiant le code d'état 200
    """
    # Enregistrer une catégorie de Faq
    ticket_category = TicketCategory.objects.create(title=secrets.token_hex(5), slug=secrets.token_urlsafe(5))

    response = client.get(reverse('faq', args=[ticket_category.slug]))

    assertTemplateUsed(response, 'main/faq.html')
    assert response.status_code == 200


@pytest.mark.django_db
def test_BookingView():
    """
    Vérifier si notre 'BookingView' renvoie le modèle 'booking.html' pour afficher le formulaire de mise à jour,
    pour la deuxième assertion, nous nous assurons que tout s'est bien passé en vérifiant le code d'état 200
    """
    # Enregistrer un scénario
    temp_scenario = Scenario.objects.create(
        title=secrets.token_hex(5),
        description=secrets.token_hex(100),
        duration=2.5,
        min_participant=2,
        max_participant=9,
        price_participant=20.5,
        slug=secrets.token_hex(5), )

    response = client.get(reverse('booking', args=[temp_scenario.slug]))

    assertTemplateUsed(response, 'main/booking.html')
    assert response.status_code == 200


@pytest.mark.django_db
def test_BookingSumView():
    """
    Vérifier si notre 'BookingSumView' renvoie le modèle 'booking_sum.html' pour afficher le formulaire de mise à jour,
    pour la deuxième assertion, nous nous assurons que tout s'est bien passé en vérifiant le code d'état 200
    """
    # Enregistrer un scénario
    temp_scenario = Scenario.objects.create(
        title=secrets.token_hex(5),
        description=secrets.token_hex(100),
        duration=2.5,
        min_participant=2,
        max_participant=9,
        price_participant=20.5,
        slug=secrets.token_hex(5), )

    # Authentifier un user
    my_admin = User.objects.create_user('test', 'test@test.com', 'test')
    client.login(username=my_admin.username, password='test')

    response = client.get(reverse('booking_sum'))

    assertTemplateUsed(response, 'main/booking_sum.html')
    assert response.status_code == 200


@pytest.mark.django_db
def test_BookingFinalView():
    """
    Vérifier si notre 'BookingFinalView' renvoie le modèle 'booking_final.html' pour afficher le formulaire de mise à jour,
    pour la deuxième assertion, nous nous assurons que tout s'est bien passé en vérifiant le code d'état 200
    """
    # Enregistrer un scénario
    temp_scenario = Scenario.objects.create(
        title=secrets.token_hex(5),
        description=secrets.token_hex(100),
        duration=2.5,
        min_participant=2,
        max_participant=9,
        price_participant=20.5,
        slug=secrets.token_hex(5), )

    # Enregistrer une séance
    temp_game = Game.objects.create(
        start_time='2023-05-08 14:00:00+01',
        end_time='2023-05-08 16:00:00+01',
        scenario=temp_scenario)

    # Authentifier un user
    my_admin = User.objects.create_user('test', 'test@test.com', 'test')
    client.login(username=my_admin.username, password='test')

    client.post(reverse('booking'),
                {'scenario': temp_scenario.slug, 'participant': secrets.randbits(2), 'start_time': temp_game.id})

    response = client.get(reverse('booking_final'))

    assertTemplateUsed(response, 'main/booking_final.html')
    assert response.status_code == 200
