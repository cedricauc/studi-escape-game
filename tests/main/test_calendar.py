import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_CalendarViewSet(client):
    """
    Dans la première assertion, nous testons si notre requête get renvoie le code d'état 200 (OK)
    Pour la deuxième assertion, nous nous assurons que notre vue renvoie le modèle calendar/calendar.html
    """
    response = client.get(reverse('calendar_api'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'calendar/calendar.html')
