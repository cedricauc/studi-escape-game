from django.urls import reverse, resolve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from main.views.api import ScenarioViewSet, BookingViewSet, GameViewSet, ScenarioRoomClueViewSet
from main.views.calendar import CalendarViewSet
from main.views.views import LoginView, RegisterView, LogoutView, ManageProfileView, HomeView, ScenarioView, FaqView, \
    BookingView, BookingSumView, BookingFinalView, ManageOrderView, PageNotFoundView


def test_home_url():
    """ Tester si la route 'home' correspond à HomeView """

    url = reverse('home')
    assert resolve(url).view_name == 'home'
    assert resolve(url), HomeView


def test_login_url():
    """ Tester si la route 'login' correspond à LoginView """

    url = reverse('login_view')
    assert resolve(url).view_name == 'login_view'
    assert resolve(url), LoginView


def test_register_url():
    """ Tester si la route 'register' correspond à RegisterView """

    url = reverse('register')
    assert resolve(url).view_name == 'register'
    assert resolve(url), RegisterView


def test_logout_url():
    """ Tester si la route 'logout' correspond à LogoutView """

    url = reverse('logout')
    assert resolve(url).view_name == 'logout'
    assert resolve(url), LogoutView


def test_manage_profile_url():
    """ Tester si la route 'manage' correspond à ManageProfileView """

    url = reverse('profile')
    assert resolve(url).view_name == 'profile'
    assert resolve(url), ManageProfileView


def test_manage_order_url():
    """ Tester si la route 'order' correspond à ManageOrderView """

    url = reverse('order')
    assert resolve(url).view_name == 'order'
    assert resolve(url), ManageOrderView


def test_scenario_url():
    """ Tester si la route 'scenario' correspond à ScenarioView """

    url = reverse('scenario', args=['scenario-test'])
    assert resolve(url).view_name == 'scenario'
    assert resolve(url), ScenarioView


def test_faq_url():
    """ Tester si la route 'faq' correspond à FaqView """

    url = reverse('faq')
    assert resolve(url).view_name == 'faq'
    assert resolve(url), FaqView


def test_booking_url():
    """ Tester si la route 'booking' correspond à BookingView """

    url = reverse('booking')
    assert resolve(url).view_name == 'booking'
    assert resolve(url), BookingView

    url = reverse('booking', args=['scenario-test'])
    assert resolve(url).view_name == 'booking'
    assert resolve(url), BookingView


def test_booking_sum_url():
    """ Tester si la route 'booking/sum' correspond à BookingSumView """

    url = reverse('booking_sum')
    assert resolve(url).view_name == 'booking_sum'
    assert resolve(url), BookingSumView


def test_booking_final_url():
    """ Tester si la route 'booking/final' correspond à BookingFinalView """

    url = reverse('booking_final')
    assert resolve(url).view_name == 'booking_final'
    assert resolve(url), BookingFinalView


def test_api_scenarios_url():
    """ Tester si la route 'api/scenarios/' correspond à ScenarioViewSet """

    url = reverse('scenario-list')
    assert resolve(url).view_name == 'scenario-list'
    assert resolve(url), ScenarioViewSet


def test_api_bookings_url():
    """ Tester si la route 'api/bookings/' correspond à BookingViewSet """

    url = reverse('booking-list')
    assert resolve(url).view_name == 'booking-list'
    assert resolve(url), BookingViewSet


def test_api_games_url():
    """ Tester si la route 'api/games/' correspond à GameViewSet """

    url = reverse('game-list')
    assert resolve(url).view_name == 'game-list'
    assert resolve(url), GameViewSet


def test_api_scenario_room_clue_url():
    """ Tester si la route 'api/clues/' correspond à ScenarioRoomClueViewSet """

    url = reverse('scenarioroomclue-list')
    assert resolve(url).view_name == 'scenarioroomclue-list'
    assert resolve(url), ScenarioRoomClueViewSet


def test_api_calendar_url():
    """ Tester si la route 'api/calendar' correspond à CalendarViewSet """

    url = reverse('calendar_api')
    assert resolve(url).view_name == 'calendar_api'
    assert resolve(url), CalendarViewSet


def test_api_token_url():
    """ Testing if the 'api/token/' route maps to our 'TokenObtainPairView' view """

    url = reverse('token_obtain_pair')
    assert resolve(url).view_name == 'token_obtain_pair'
    assert resolve(url).func.view_class, TokenObtainPairView


def test_api_token_refresh_url():
    """ Testing if the 'api/token/refresh/' route maps to our 'TokenRefreshView' view """

    url = reverse('token_refresh')
    assert resolve(url).view_name == 'token_refresh'
    assert resolve(url).func.view_class, TokenRefreshView