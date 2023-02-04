import secrets
import pytest
from django.contrib import auth
from django.test import Client
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed
from main.models import User, Scenario, TicketCategory, Game


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def credentials():
    credentials = {
        'first_name': 'test',
        'last_name': 'test',
        'username': 'test@testing.com',
        'email': 'test@testing.com',
        'password': 'TestPassword',
        'confirmation': 'TestPassword'
    }
    return credentials


@pytest.fixture
def login(credentials, client):
    temp_user = client.post(reverse('register'), credentials)
    client.post(reverse('login_view'), {'username': 'TestUser', 'password': 'TestPassword'})
    return temp_user


@pytest.fixture
def scenario():
    temp_scenario = Scenario.objects.create(
        title=secrets.token_hex(5),
        description=secrets.token_hex(100),
        duration=2.5,
        min_participant=2,
        max_participant=9,
        price_participant=20.5,
        slug=secrets.token_hex(5)
    )
    return temp_scenario


@pytest.fixture
def game(scenario):
    temp_game = Game.objects.create(
        start_time='2023-05-08 14:00:00+01',
        end_time='2023-05-08 16:00:00+01',
        scenario=scenario)
    return temp_game


@pytest.fixture
def category():
    temp_category = TicketCategory.objects.create(title=secrets.token_hex(5), slug=secrets.token_urlsafe(5))
    return temp_category


@pytest.mark.django_db
def test_HomeView(client, scenario):
    """ 
    Dans la première assertion, nous testons si notre requête get renvoie le code d'état 200 (OK)
    Pour la deuxième assertion, nous nous assurons que notre vue renvoie le modèle home.html
    """
    scenario.save()
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'main/index.html')


@pytest.mark.django_db
def test_RegisterView(client, credentials):
    """
    In the first assert, we are checing if a user is created successfully then, the user is redirected to '/login/' route,
    For the second assert, we are checking the 302 status code(redirect)
    """
    response = client.post(reverse('register'), credentials)

    assert response.url == reverse('home')
    assert response.status_code == 302


@pytest.mark.django_db
def test_LoginView(client, credentials):
    """
    Dans la première assertion, nous vérifions si un utilisateur est créé avec succès, puis l'utilisateur est redirigé vers la route '/login/',
    Pour la deuxième assertion, nous vérifions le code d'état 302 (redirection)
    """
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
def test_LogoutView(client):
    """
    Tester si notre LogoutView déconnecte correctement l'utilisateur, Dans la première assertion, nous vérifions si l'utilisateur est redirigé vers
    route d'accueil, pour la deuxième affirmation, nous vérifions le code d'état de redirection 302
    """
    response = client.get(reverse('logout'))

    assert response.url == reverse('home')
    assert response.status_code == 302


@pytest.mark.django_db
def test_ManageProfileView(login, client):
    """
    Tester si ManageProfileView est rendu correctement en vérifiant le code d'état 200,
    Pour la deuxième assertion, nous nous assurons que le modèle 'profile.html' est rendu
    """
    response = client.get(reverse('profile'))

    assert response.status_code == 200
    assertTemplateUsed(response, 'main/profile.html')


@pytest.mark.django_db
def test_ManageOrderView(login, client):
    """
    Vérifier si notre 'ManageOrderView' renvoie le modèle 'order.html' pour afficher le formulaire de mise à jour,
    pour la deuxième assertion, nous nous assurons que tout s'est bien passé en vérifiant le code d'état 200
    """
    response = client.get(reverse('order'))

    assertTemplateUsed(response, 'main/order.html')
    assert response.status_code == 200


@pytest.mark.django_db
def test_ScenarioView(client, scenario):
    """
    Vérifier si notre 'ScenarioView' renvoie le modèle 'scenario.html' pour afficher le formulaire de mise à jour,
    pour la deuxième assertion, nous nous assurons que tout s'est bien passé en vérifiant le code d'état 200
    """
    response = client.get(reverse('scenario', args=[scenario.slug]))

    assertTemplateUsed(response, 'main/scenario.html')
    assert response.status_code == 200


@pytest.mark.django_db
def test_FaqView(client):
    """
    Vérifier si notre 'FaqView' renvoie le modèle 'scenario.html' pour afficher le formulaire de mise à jour,
    pour la deuxième assertion, nous nous assurons que tout s'est bien passé en vérifiant le code d'état 200
    """
    # Enregistrer une catégorie de Faq
    ticket_category = TicketCategory.objects.create(title=secrets.token_hex(5), slug=secrets.token_urlsafe(5))

    response = client.get(reverse('faq'))

    assertTemplateUsed(response, 'main/faq.html')
    assert response.status_code == 200


@pytest.mark.django_db
def test_BookingView(client, scenario):
    """
    Vérifier si notre 'BookingView' renvoie le modèle 'booking.html' pour afficher le formulaire de mise à jour,
    pour la deuxième assertion, nous nous assurons que tout s'est bien passé en vérifiant le code d'état 200
    """
    response = client.get(reverse('booking', args=[scenario.slug]))

    assertTemplateUsed(response, 'main/booking.html')
    assert response.status_code == 200


@pytest.mark.django_db
def test_BookingSumView(login, client, scenario):
    """
    Vérifier si notre 'BookingSumView' renvoie le modèle 'booking_sum.html' pour afficher le formulaire de mise à jour,
    pour la deuxième assertion, nous nous assurons que tout s'est bien passé en vérifiant le code d'état 200
    """
    response = client.get(reverse('booking_sum'))

    assertTemplateUsed(response, 'main/booking_sum.html')
    assert response.status_code == 200


@pytest.mark.django_db
def test_BookingFinalView(login, client, scenario, game):
    """
    Vérifier si notre 'BookingFinalView' renvoie le modèle 'booking_final.html' pour afficher le formulaire de mise à jour,
    pour la deuxième assertion, nous nous assurons que tout s'est bien passé en vérifiant le code d'état 200
    """
    client.post(reverse('booking'),
                {'scenario': scenario.slug, 'participant': 3, 'start_time': game.id})

    response = client.get(reverse('booking_final'))

    assertTemplateUsed(response, 'main/booking_final.html')
    assert response.status_code == 200


@pytest.mark.django_db
def test_booking_success(login, client, scenario, game):
    """
    Pour la première assertion, nous nous assurons que la réservation d'une séance a été ajouté au panier,
    et nous vérifions le code d'état de redirection 302.
    Pour la deuxième assertion, nous nous assurons que l'utilisateur a pris connaissance,
    et accepte le montant total de la réservation et nous vérifions le code d'état de redirection 302.
    Pour la troisième assertion, nous nous assurons que l'utilisateur accepte les conditions d'achat,
    et nous vérifions le code d'état de redirection 302.
    """
    response = client.post(
        reverse('booking'), {'scenario': scenario.slug, 'participant': secrets.randbits(2), 'start_time': game.id})

    assert response.url == reverse('booking_sum')
    assert response.status_code == 302

    response = client.post(
        reverse('booking_sum'), {'checkout': True})

    assert response.url == reverse('booking_final')
    assert response.status_code == 302

    response = client.post(
        reverse('booking_final'), {'tos': True})

    assert response.url == reverse('order')
    assert response.status_code == 302


@pytest.mark.django_db
def test_booking_failure(login, client, scenario, game):
    """
    Pour la première assertion, nous nous assurons que la réservation d'une séance a été ajouté au panier,
    et nous vérifions le code d'état de redirection 302.
    Pour la deuxième assertion, nous nous assurons que l'utilisateur a pris connaissance,
    et accepte le montant total de la réservation et nous vérifions le code d'état de redirection 302.
    Pour la troisième assertion, nous nous assurons que l'utilisateur n'accepte pas les conditions d'achat,
    et nous vérifions le code d'état de 200.
    """
    response = client.post(
        reverse('booking'), {'scenario': scenario.slug, 'participant': secrets.randbits(2), 'start_time': game.id})

    assert response.url == reverse('booking_sum')
    assert response.status_code == 302

    response = client.post(
        reverse('booking_sum'), {'checkout': True})

    assert response.url == reverse('booking_final')
    assert response.status_code == 302

    response = client.post(
        reverse('booking_final'))

    assertTemplateUsed(response, 'main/booking_final.html')
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_ticket_faq(login, client, category):
    """
    Pour la première assertion, nous nous assurons qu'un ticket est créé pour la faq,
    et nous vérifions le code d'état 200.
    Pour la deuxième assertion, nous nous assurons qu'un ticket faq a été enregistrer en base de données.
    Pour la troisième assertion, nous vérifions le code d'état 200.
    """
    response = client.post(
        reverse('faq'), {'author':secrets.token_hex(10), 'category': category, 'question': secrets.token_hex(100)})

    assertTemplateUsed(response, 'main/faq.html')
    assert response.status_code == 200

    response = client.get(
        reverse('faq'))

    assert len(TicketCategory.objects.all()) == 1

    assertTemplateUsed(response, 'main/faq.html')
    assert response.status_code == 200
    