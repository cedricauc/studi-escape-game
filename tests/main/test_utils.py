import pytest
from datetime import datetime, date, timedelta

from main.utils.util import create_booking_number, day_beginning, day_end, time_conversion


def test_create_booking_numbe():
    """
    test de la fonction creat_booking_number
    """
    scenario_title = "La prison maudite du Hollandais Volant"
    today = date.today()
    first_letters = "".join(word[0].upper() for word in scenario_title.split())
    booking_number = first_letters + today.strftime("%d%m%Y%H%M")
    assert booking_number == create_booking_number(scenario_title)


def test_day_beginning():
    """
    test de la fonction day_beginning
    """
    dt = datetime(2023, 1, 2)
    assert "02-01-2023 00:00:00" == day_beginning(dt).strftime("%d-%m-%Y %H:%M:%S")


def test_day_end():
    """
    test de la fonction day_end
    """
    dt = datetime(2023, 1, 2)
    assert "02-01-2023 23:59:00" == day_end(dt).strftime("%d-%m-%Y %H:%M:%S")


def test_time_conversion():
    """
    test de la fonction time_conversion
    """
    assert {30, 0} == time_conversion(1800)  # 0.5 heures = 1800 secondes
    assert {0, 2} == time_conversion(7200)  # 2 heures = 7200 secondes
    assert {30, 2} == time_conversion(9000)  # 2.5 heures = 9000 secondes
