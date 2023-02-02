from django.contrib.auth.models import User

import secrets
import pytest

from main.models import User, Level, Image, Room, Scenario, Game, Cart, Booking, Discount, ScenarioRoomClue, \
    TicketCategory, TicketQuestion, TicketAnswer


@pytest.mark.django_db
def test_user_str():
    """
    Tester si la méthode User's __str__ est correctement implémentée
    """
    user = User.objects.create(username='TestUser', password='random_password', email='TestUser@domain.com')

    assert str(user) == f"Profil de {user.get_full_name()}"


@pytest.mark.django_db
def test_level_str():
    """
    Tester si la méthode Level's __str__ est correctement implémentée
    """
    level = Level.objects.create(name='TestLevel')

    assert str(level) == level.name


@pytest.mark.django_db
def test_image_str():
    """
    Tester si la méthode Image's __str__ est correctement implémentée
    """
    image = Image.objects.create(title=secrets.token_hex(5), alt=secrets.token_hex(5))

    assert str(image) == image.title


@pytest.mark.django_db
def test_room_str():
    """
    Tester si la méthode Room's __str__ est correctement implémentée
    """
    room = Room.objects.create(num=secrets.token_hex(5))

    assert str(room) == room.num


@pytest.mark.django_db
def test_scenario_str():
    """
    Tester si la méthode Scenario's __str__ est correctement implémentée
    """
    scenario = Scenario.objects.create(
        title=secrets.token_hex(5),
        description=secrets.token_hex(100),
        duration=2.5,
        min_participant=2,
        max_participant=9,
        price_participant=20.5,
        slug=secrets.token_hex(5),
    )

    assert str(scenario) == scenario.title


@pytest.mark.django_db
def test_game_str():
    """
    Tester si la méthode Game's __str__ est correctement implémentée
    """
    scenario = Scenario.objects.create(
        title=secrets.token_hex(5),
        description=secrets.token_hex(100),
        duration=2.5,
        min_participant=2,
        max_participant=9,
        price_participant=20.5,
        slug=secrets.token_urlsafe(5)
    )

    game = Game.objects.create(
        start_time='2023-05-08 14:00:00+01',
        end_time='2023-05-08 16:00:00+01',
        scenario=scenario
    )

    assert str(game) == f"{scenario.title} commence à {game.start_time} et fini à {game.end_time}"


@pytest.mark.django_db
def test_cart_str():
    """
    Tester si la méthode Cart's __str__ est correctement implémentée
    """
    user = User.objects.create(username='TestUser', password='random_password', email='TestUser@domain.com')

    scenario = Scenario.objects.create(title=secrets.token_hex(5), description=secrets.token_hex(100))

    game = Game.objects.create(
        start_time='2023-05-08 14:00:00+01',
        end_time='2023-05-08 16:00:00+01',
        scenario=scenario
    )

    cart = Cart.objects.create(game=game, user=user)

    assert str(cart) == f"scenario {scenario.title} par {user.get_full_name()} à {cart.created_date}"


@pytest.mark.django_db
def test_booking_str():
    """
    Tester si la méthode Booking's __str__ est correctement implémentée
    """
    user = User.objects.create(username='TestUser', password='random_password', email='TestUser@domain.com')

    scenario = Scenario.objects.create(title=secrets.token_hex(5), description=secrets.token_hex(100))

    game = Game.objects.create(
        start_time='2023-05-08 14:00:00+01',
        end_time='2023-05-08 16:00:00+01',
        scenario=scenario
    )

    booking = Booking.objects.create(
        booking_number=secrets.token_hex(5),
        total_amount=secrets.randbits(5),
        game=game,
        user=user
    )

    assert str(booking) == f"profile {user.get_full_name()} a reservé {game.scenario.title} le {game.start_time}"


@pytest.mark.django_db
def test_discount_str():
    """
    Tester si la méthode Discount's __str__ est correctement implémentée
    """
    scenarios = [Scenario.objects.create(title=secrets.token_hex(5), description=secrets.token_hex(100)),
                 Scenario.objects.create(title=secrets.token_hex(5), description=secrets.token_hex(100))]

    discount = Discount.objects.create(
        step=secrets.randbits(2),
        discount=secrets.randbits(2),
        is_percentage=False,
    )

    for scenario in scenarios:
        discount.scenarios.add(scenario)

    assert str(
        discount) == f"remise de {discount.discount} appliqué sur {len(discount.scenarios.all())} scenarios"


@pytest.mark.django_db
def test_scenario_room_clue_str():
    """
    Tester si la méthode ScenarioRoomClue's __str__ est correctement implémentée
    """
    scenario = Scenario.objects.create(title=secrets.token_hex(5), description=secrets.token_hex(100))

    room = Room.objects.create(num=secrets.token_hex(5))

    scenario_room_clue = ScenarioRoomClue.objects.create(
        clue=secrets.token_hex(100),
        scenario=scenario,
        room=room
    )

    assert str(scenario_room_clue) == f"indice {scenario_room_clue.id} pour le scénario {scenario.title} dans la pièce {room.num}"


@pytest.mark.django_db
def test_ticket_category():
    """
    Tester si la méthode TicketCategory's __str__ est correctement implémentée
    """
    ticket_category = TicketCategory.objects.create(title=secrets.token_hex(5), slug=secrets.token_urlsafe(5))

    assert str(ticket_category) == ticket_category.title


@pytest.mark.django_db
def test_ticket_question():
    """
    Tester si la méthode TicketQuestion's __str__ est correctement implémentée
    """
    ticket_category = TicketCategory.objects.create(title=secrets.token_hex(5), slug=secrets.token_urlsafe(5))

    ticket_question = TicketQuestion.objects.create(
        author=secrets.token_hex(5),
        question=secrets.token_hex(10),
        category=ticket_category)

    assert str(ticket_question) == f"billet de {ticket_question.author} sur {ticket_category.title}"


@pytest.mark.django_db
def test_ticket_answer():
    """
    Tester si la méthode TicketAnswer's __str__ est correctement implémentée
    """
    ticket_category = TicketCategory.objects.create(title=secrets.token_hex(5), slug=secrets.token_urlsafe(5))

    ticket_question = TicketQuestion.objects.create(
        author=secrets.token_hex(5),
        question=secrets.token_hex(10),
        category=ticket_category)

    ticket_answer = TicketAnswer.objects.create(
        answer=secrets.token_hex(10),
        question=ticket_question
    )

    assert str(ticket_answer) == f"réponse {ticket_answer.id} du billet {ticket_question.id}"