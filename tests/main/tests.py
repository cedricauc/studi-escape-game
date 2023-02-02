import pytest
import decimal

from django.shortcuts import resolve_url
from django.urls import reverse
from django.test import Client
from django.contrib import auth
from main.models import Scenario, Cart, Booking, Level, Room, User, Game


@pytest.mark.django_db
def test_booking_saved_correctly():
    u = User(
        first_name="test",
        last_name="test",
        username="test@gmail.com",
        email="test@gmail.com",
        role=2
    )
    u.save()

    lvl = Level(name="Intermediare")
    lvl.save()
    r1 = Room(num="111")
    r1.save()
    s = Scenario(
        title="La prison maudite du Hollandais Volant",
        description="Résoudre des énigmes de la prison maudite du Hollandais Volant en cherchant des indices,"
                    " des clés, des passages secrets et en fouillant le décor dans les moindres recoins.",
        duration=2.5,
        min_participant=3,
        max_participant=5,
        price_participant=35.0,
        slug="prison-maudite",
        level=lvl,
    )
    s.save()

    g = Game(
        start_time="2022-10-12 10:00:00+02",
        end_time="2022-10-12 13:00:00+02",
        scenario=s
    )
    g.save()

    c = Cart(
        participant=2,
        game=g,
        user=u
    )
    c.save()

    b = Booking(
        booking_number="ABC1234",
        participant=c.participant,
        total_amount=c.participant * s.price_participant,
        game=g,
        user=u
    )
    b.save()

    saved = Booking.objects.get(booking_number="ABC1234")
    assert saved == b
    assert saved.total_amount == decimal.Decimal("70.0")
    assert saved.game.scenario.title == "La prison maudite du Hollandais Volant"
    assert saved.game.scenario.level.name == "Intermediare"
    assert saved.user.username == "test@gmail.com"


@pytest.mark.django_db
def test_login_route():
    client = Client()

    # Inscrire un utilisateur à l’aide de la vue `signup`afin de l’enregistrer dans la base de données
    credentials = {
        'first_name': 'test',
        'last_name': 'test',
        'username': 'test@testing.com',
        'email': 'test@testing.com',
        'password': 'TestPassword',
        'confirmation': 'TestPassword'
    }
    temp_user = client.post(reverse('register'), credentials)

    # Connecter cet utilisateur avec la vue `login`
    response = client.post(reverse('login_view'),
                           {'username': 'test@testing.com', 'password': 'TestPassword', 'next': 'None'})

    # Vérifier que la redirection vers la page d’accueil est effectuée
    assert response.status_code == 302
    assert response.url == reverse('home')

    # Vérifier que l’utilisateur est bien authentifié
    user = auth.get_user(client)
    assert user.is_authenticated


@pytest.mark.django_db
def test_scenario_route():
    # Créer un superuser
    my_admin = User.objects.create_superuser('test', 'test@test.com', 'test')

    client = Client()

    # Authentifier un superuser
    client.login(username=my_admin.username, password='test')

    scenario = {
        'title': 'scenario test',
        'description': 'scenario test',
        'duration': 3,
        'min_participant': 1,
        'max_participant': 9,
        'price_participant': 99,
        'slug': 'scenario-test'
    }
    temp_scenario = client.post('/api/scenarios/', data=scenario)
    assert temp_scenario.status_code == 201

    # Requete pour la vue `scenario`
    response = client.get(resolve_url('scenario', slug='scenario-test'))
    assert response.status_code == 200
