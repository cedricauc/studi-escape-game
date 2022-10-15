import calendar

from django.db.models import Q

from main.models import Scenario, Cart, Discount, Booking
from datetime import datetime, date, timedelta


def footer_scenario(request):
    """
    Retourne liste des scénarios
    """
    return {'footer_scenario': Scenario.objects.all()}


def prepare_booking(cart_id):
    """
    Retourne une liste de variables pour finaliser une réservation
    """
    cart = Cart.objects.get(pk=cart_id)

    discounts = Discount.objects.filter(scenarios__games__cart__exact=cart)

    total = cart.game.scenario.price_participant * cart.participant
    discount = 0
    for row in discounts.order_by("-discount"):
        if cart.participant >= row.step:
            if row.is_percentage:
                discount = round((total * (row.discount / 100)), 2)
            else:
                discount = row.discount
            break
    total_amount = total - discount

    return [cart, discount, total, total_amount]


def create_booking_number(scenario_title):
    """
    Retourne une chaîne de caractère correspondant à un identifiant de réservation
    """
    today = date.today()
    first_letters = "".join(word[0].upper() for word in scenario_title.split())
    return first_letters + today.strftime("%d%m%Y%H%M")


def get_date(req_day):
    """
    Retoure la date du jour
    """
    if req_day:
        year, month, day = (int(x) for x in req_day.split('-'))
        return date(year, month, day)
    return datetime.today()


def prev_month(d):
    """
    Retourne la date du mois précédent
    """
    first = d.replace(day=1)
    month = first - timedelta(days=1)
    return month


def next_month(d):
    """
    Retourne la date du mois prochain
    """
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    month = last + timedelta(days=1)
    return month


def exclude_booked_events(events):
    time_threshold = datetime.now() - timedelta(minutes=1)

    events = events.exclude(
        Q(id__in=Booking.objects.filter(is_canceled=False).values_list('game_id', flat=True).all()) |
        Q(id__in=Cart.objects.filter(created_date__time__gt=time_threshold).values_list('game_id', flat=True).all())
    )

    return events
